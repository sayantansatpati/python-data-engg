__author__ = 'ssatpati'

import db


def db_pkg_test():
    mConn = db.DB(filename='baseball-archive-2012.sqlite', dbtype='sqlite')
    print(mConn.tables)

    print(mConn.find_column('*ID'))

    print(mConn.tables.Schools)
    print(mConn.tables.Schools.sample())

    print(mConn.tables.SchoolsPlayers)
    print(mConn.tables.SchoolsPlayers.sample())

    #print(mConn.tables.AllstarFull.sample())


    print(mConn.query("""
SELECT * FROM AllstarFull
    where AllstarFull.yearID=1995
    """))


    '''
    print(mConn.tables.Artist.head())
    print(mConn.tables.Album.head())
    '''



if __name__ == '__main__':
    db_pkg_test()
