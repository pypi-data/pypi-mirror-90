import glob
import os
import pymysql # pip install pymysql # pylint: disable=import-error
import json

from msbase.logging import logger
from msbase.utils import getenv
from path import Path # pip install path # pylint: disable=import-error

def prepare_insert_query(row_dict, table, ignore_dup = False):
    row_items = list(row_dict.items())
    fields = ", ".join([ k for k, v in row_items ])
    placeholders = ", ".join([ "%s" for k, v in row_items ])
    values = tuple(v for k, v in row_items)
    ignore = ""
    if ignore_dup:
        ignore = "IGNORE"
    return "INSERT %s INTO %s (%s) VALUES (%s)" % (ignore, table, fields, placeholders), values

def decode_entry(entry):
    if entry is None: return None
    for col in entry.keys():
        if col.endswith("_json"):
            entry[col] = json.loads(entry[col])
    return entry

class DB(object):
    def __init__(self, config_dir: str, db_config):
        print("Connecting DB")
        with Path(config_dir):
            self.db_ = pymysql.connect(**db_config)

    def db(self):
        return self.db_

    def exec(self, query, args=()):
        self.db().ping(reconnect=True)
        with self.db().cursor() as cur:
            logger.info(query % args)
            cur.execute(query, args)
        self.commit()

    def exec_fetch(self, query, args=(), mode=str, return_dict=False, do_commit=True):
        self.db().ping(reconnect=True)
        assert mode in ["one", "all"]
        if return_dict:
            cur = self.db().cursor(pymysql.cursors.DictCursor)
        else:
            cur = self.db().cursor()
        cur.execute(query, args)
        if mode == "one":
            ret = cur.fetchone()
        else:
            ret = cur.fetchall()
        cur.close()
        if do_commit:
            self.commit()
        return ret

    def exec_fetch_one(self, query, args=(), return_dict=False, do_commit=True):
        return self.exec_fetch(query, args, mode="one", return_dict=return_dict, do_commit=do_commit)

    def exec_fetch_all(self, query, args=(), return_dict=False):
        return self.exec_fetch(query, args, mode="all", return_dict=return_dict)

    def upgrade(self):
        SCHEMA_DIR = getenv("SCHEMA_DIR")

        max_version = "1000"
        cur = self.db().cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS metadata (`version` TEXT NOT NULL)")
        cur.execute("SELECT `version` FROM metadata")
        ret_all = cur.fetchall()
        cur.close()
        assert len(ret_all) <= 1
        if len(ret_all) == 0:
            cur = self.db().cursor()
            cur.execute("INSERT INTO metadata (`version`) VALUES (%s)" % max_version)
            cur.close()
        else:
            max_version = ret_all[0][0]
        for f in sorted(glob.glob(SCHEMA_DIR + "/*.sql")):
            current_version = os.path.basename(f).split("-")[0]
            if current_version > max_version:
                cur = self.db().cursor()
                query = open(f, "r").read()
                print(query)
                cur.execute(query)
                max_version = max(current_version, max_version)
                cur.close()
        cur = self.db().cursor()
        cur.execute("UPDATE metadata SET `version` = %s" % max_version)
        cur.close()
        self.commit()

    def insert_row(self, row_dict, table, ignore_dup = False):
        query, values = prepare_insert_query(row_dict, table, ignore_dup=ignore_dup)
        self.exec(query, values)

    def insert_row_get_id(self, row_dict, table):
        self.db().ping(reconnect=True)
        cur = self.db().cursor()
        query, values = prepare_insert_query(row_dict, table)
        logger.info(query)
        cur.execute(query, values)
        cur.execute("SELECT LAST_INSERT_ID()")
        ret = cur.fetchone()[0]
        cur.close()
        self.commit()
        return ret

    def commit(self):
        self.db().commit()
