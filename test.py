#!/usr/bin/env python

# global variables
import sys, os
base = os.path.dirname(os.path.realpath(__file__))
env  = os.path.join(base, 'env')

# determine the virtual python executable
INTERP = os.path.join(env, 'bin', 'python')
if not os.path.exists(INTERP):
    INTERP = os.path.join(env, 'Scripts', 'python.exe')

# ensure we found it
if not os.path.exists(INTERP):
    print 'Unable to determine virtual python executable location.'
    sys.exit(1)

# run the process from the virtual python env
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# update the sys path
sys.path.insert(0, base)

# coverage and unittesting
import unittest
from coverage import coverage
cov = coverage(branch = True, omit = ['env/*', 'test.py', 'manage.py'])
cov.start()

# create our app
from pickpicks.configs import ConfigUnitTesting

# get the database and models
from pickpicks.database import Base
from pickpicks.models import User, League, Team, Sport, Game, Pick, LeagueUserAssociation, UserConfirmation

class TestCase(unittest.TestCase):
    def setUp(self):
        # create the application
        from pickpicks import create_app
        self.app = create_app(ConfigUnitTesting).test_client()

        # connect to the database
        from sqlalchemy.engine import create_engine
        engine = create_engine(ConfigUnitTesting.SQLALCHEMY_DATABASE_URI)
        self.db = Base.metadata
        self.db.bind = engine

        # create the sesssion
        from sqlalchemy.orm import sessionmaker
        db_session = sessionmaker(
                autocommit=False,
                bind=engine)
        self.session = db_session()

        # create the database
        self.db.create_all()

    def tearDown(self):
        self.db.drop_all()

    ###############################
    # HELPER FUNCTIONS
    ###############################

    def create_user(self, username, email='test@test.com'):
        '''Creates a user with a specific name.'''
        user = User(email=email, password='password', username=username)
        conf = user.get_confirmation()
        self.session.add(user)
        self.session.add(conf)
        self.session.commit()
        return user

    def create_league(self, commissioner, name):
        '''Createas a league with the specified commissioner.'''
        league = League(name=name, commissioner=commissioner)
        self.session.add(league)
        self.session.commit()
        return league

    def create_sport(self, name):
        '''Creates a sport.'''
        sport = Sport(name=name)
        self.session.add(sport)
        self.session.commit()
        return sport

    def create_team(self, sport, name):
        '''Creates a team.'''
        team = Team(name=name, sport=sport)
        self.session.add(team)
        self.session.commit()
        return team

    def create_game(self, sport, home, away):
        game = Game(sport=sport, home=home, away=away)
        self.session.add(game)
        self.session.commit()
        return game

    def create_pick(self, user, league, game):
        pick = Pick(user=user, league=league, game=game)
        self.session.add(pick)
        self.session.commit()
        return pick

class UserTestCase(TestCase):
    def test_user(self):
        '''Tests creating a user, which will be used later.'''
        u = self.create_user(username='test')

        # this failing really kills us
        assert u.id == 1
        assert u.username == 'test'
        assert u.confirmation != None
        assert u.is_confirmed() == False
        assert u.confirmation == u.get_confirmation()

        # confirm it
        u.confirmation.confirmed = True
        self.session.commit()
        u = self.session.query(User).first()
        assert u.is_confirmed() == True

class LeagueTestCase(TestCase):
    def test_league(self):
        self.tearDown()
        self.setUp()

        u = self.create_user(username='test')
        l = self.create_league(commissioner=u, name='test')

        assert l.commissioner_id == 1
        assert l.name == 'test'
        assert l.commissioner == u
        assert u.commissionerof[0] == l

    def test_add_user(self):
        self.tearDown()
        self.setUp()

        # setup the league
        u1 = self.create_user(username='test1')
        u2 = self.create_user(username='test2', email='test2@test.com')
        l = self.create_league(commissioner=u1, name='test')

        # create the user association
        a = LeagueUserAssociation(u2, l)
        self.session.add(a)
        self.session.commit()

        assert l.users[0].user == u2
        assert u2.leagues[0].league == l

class PickTestCase(TestCase):
    def test_pick(self):
        u = self.create_user(username='test')
        l = self.create_league(commissioner=u, name='test')
        s = self.create_sport(name='Baseball')
        h = self.create_team(sport=s, name='Yankees')
        a = self.create_team(sport=s, name='Red Sox')
        g = self.create_game(sport=s, home=h, away=a)
        p = self.create_pick(user=u, league=l, game=g)

        assert p.id == 1
        assert p.pick == 1
        assert p.user == u
        assert p.user_id == 1
        assert p.league == l
        assert p.league_id == 1
        assert p.game == g
        assert p.game_id == 1
        assert u.picks[0] == p
        assert l.picks[0] == p
        assert g.picks[0] == p

class GameTestCase(TestCase):
    def test_game(self):
        s = self.create_sport(name='Baseball')
        h = self.create_team(sport=s, name='Yankees')
        a = self.create_team(sport=s, name='Red Sox')
        g = self.create_game(sport=s, home=h, away=a)

        assert g.id == 1
        assert g.sport == s
        assert g.home == h
        assert g.away == a
        assert g.sport_id == 1
        assert g.home_id == 1
        assert g.away_id == 2
        assert h.games[0] == g
        assert a.games[0] == g
        assert h.home_games[0] == g
        assert a.away_games[0] == g

class TeamTestCase(TestCase):
    def test_team(self):
        s = self.create_sport(name='Baseball')
        t = self.create_team(sport=s, name='Yankees')

        assert t.id == 1
        assert t.name == 'Yankees'
        assert t.sport == s
        assert t.sport_id == 1

class SportTestCase(TestCase):
    def test_sport(self):
        s = self.create_sport('Baseball')
        self.session.add(s)
        self.session.commit()

        assert s.id == 1
        assert s.name == 'Baseball'

if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass

    # print the coverage report
    cov.stop()
    cov.save()
    print '\n\nCoverage Report:\n'
    cov.report()

    # save an HTML coverage report
    print 'HTML version: ' + os.path.join(base, 'coverage/index.html')
    cov.html_report(directory='coverage')
    cov.erase()
