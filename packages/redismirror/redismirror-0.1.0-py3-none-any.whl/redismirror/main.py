import click
import sys
import redis
from time import sleep
import re
from redismirror.redisCommand import *
import threading

# TO DO:
# 3. Support to split it to multi node
# 4. Support most of redis command


@click.command()
@click.option(
    "--host", type=str, default="127.0.0.1", help="Destination redis host/IP."
)
@click.option("--port", type=int, default=6379, help="Destination redis port.")
@click.option(
    "--db", type=int, default="0", required=False, help="Destination redis DB."
)
@click.option(
    "--auth",
    default=None,
    type=str,
    required=False,
    help="Destination redis auth info.",
)
@click.option("--counter", type=int, required=False, help="number of keys to mirror.")
def main(host, port, db, auth, counter):
    r = makeConnection(host, port, db, auth)
    getSTDOUT(r, counter)


def makeConnection(host, port, db, auth):
    """Function to create redis connection

    Note:
        If the connection failed, the program will exit 1

    Args:
        host (str): redis connection string
        port (int): redis port number
        db (int): redis database name
        auth (str): auth info for redis

    Returns:
        connection: connection object for redis
    """
    if auth:
        pool = redis.ConnectionPool(host=host, port=port, db=db, password=auth)
    else:
        pool = redis.ConnectionPool(host=host, port=port, db=db)
    r = redis.StrictRedis(connection_pool=pool)
    try:
        r.ping()
        print("Redis is connected..")
    except Exception as e:
        print(f"Redis connection error ({e})")
        sys.exit(1)
    return r


def getSTDOUT(connection, counter):
    if not sys.stdin.isatty():
        input_stream = sys.stdin
    else:
        print("There is no stdin, check help for more info. exit 1")
        sys.exit(1)
    timerCounter = 0
    for line in input_stream:
        try:
            timerCounter = timerCounter + 1
            if not timerCounter == counter:
                tmpLine = line.split(" ", 5)
                keyType = str(tmpLine[3]).strip('"')
                if keyType == "set":
                    setFunc(line, connection)
                elif keyType == "hset":
                    hsetFunc(line, connection)
                else:
                    print(f"key type ({keyType}) if not supported yet.")
            else:
                print(f"Finished at count {timerCounter}")
                sys.exit(0)
        except Exception as e:
            print(f"Skip line({line[:30]})")


if __name__ == "__main__":
    main()