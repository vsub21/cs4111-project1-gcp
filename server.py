#!/usr/bin/env python2.7

"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

DATABASEURI = "postgresql://vs2575:0700@35.196.90.148/proj1part2"

engine = create_engine(DATABASEURI)

isDBA = False

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None


@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


@app.route('/')
def signin():
  global isDBA
  isDBA = False
  print "at signin(), dba is " + str(isDBA)
  return render_template('signin.html', isDBA=isDBA)


@app.route('/enable_dba')
def enable_dba():
  global isDBA
  isDBA = True
  print "at enable_dba(), dba is " + str(isDBA)
  return render_template('index.html', isDBA=isDBA)


@app.route('/signout')
def signout():
  global isDBA
  isDBA = False
  print "at signout(), dba is " + str(isDBA)
  return render_template('signin.html', isDBA=isDBA)


@app.route('/index')
def index():
  print request.args
  print "at index(), dba is " + str(isDBA)
  return render_template('index.html', isDBA=isDBA)


def process_cursor(cursor, col_titles):
  result = []

  for row in cursor:
    row_string = str(row)
    row_string = row_string[3:-4]
    row_string = row_string.split(',')
    result.append(row_string)

  if (col_titles is not None):
    return pd.DataFrame(np.array(result), columns=col_titles)

  return pd.DataFrame(np.array(result))

@app.route('/coach', methods=['GET', 'POST'])
def coach():
  global isDBA
  print "at coach(), dba is " + str(isDBA)
  if request.method == 'POST':
    coach_id = request.form['coach_id']
    fname = request.form['fname']
    lname = request.form['lname']
    sex = request.form['sex']
    dob = request.form['dob']
    c_wins = request.form['c_wins']
    c_losses = request.form['c_losses']

    s = "INSERT INTO coach (coach_id, fname, lname, sex, dob, c_wins, c_losses) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(coach_id, fname, lname, sex, dob, c_wins, c_losses)
    print s
    g.conn.execute(s)

  sel_st = "SELECT coach_id, fname, lname, sex, dob, c_wins, c_losses FROM coach"

  cursor = g.conn.execute(sel_st)
  results = []

  for row in cursor:
        results.append(row)
  cursor.close()

  print results

  context = dict(data = results)
  print context

  return render_template('coach.html', isDBA=isDBA, **context)

@app.route('/search_coach', methods=['GET', 'POST'])
def search_coach():
  global isDBA
  if request.method == 'POST':
    fname = request.form['coach_fname']
    lname = request.form['coach_lname']

    sel_st = """
    SELECT coach_id AS "Coach ID", fname AS "First Name", lname AS "Last Name", sex AS "Sex", dob AS "Date of Birth", c_wins AS "Career Wins", c_losses AS "Career Losses"
    FROM coach C
    WHERE fname = '{}' AND lname = '{}'
    """.format(fname, lname)

  cursor = g.conn.execute(sel_st)
  results = []
  cursor = g.conn.execute(sel_st)

  for row in cursor:
        results.append(row)
  cursor.close()

  print results

  context = dict(data = results)

  return render_template('search.html', isDBA=isDBA, **context)

@app.route('/court', methods=['GET', 'POST'])
def court():
  if request.method == 'POST':
    court_id = request.form['court_id']
    city = request.form['city']
    state = request.form['state']
    zipcode = request.form['zipcode']

    s = "INSERT INTO court (court_id, city, state, zipcode) VALUES ('{}', '{}', '{}', '{}')".format(court_id, city, state, zipcode)
    print s
    g.conn.execute(s)


  sel_st = "SELECT court_id, city, state, zipcode FROM court"
  col_titles = ['Court ID', 'City', 'State', 'Zipcode']

  cursor = g.conn.execute(sel_st)
  results = []
  cursor = g.conn.execute(sel_st)

  for row in cursor:
      results.append(row)
  cursor.close()

  print results

  context = dict(data = results)

  return render_template('court.html', isDBA=isDBA, **context)


@app.route('/dba', methods=['GET', 'POST'])
def dba():
  # invalidEntry = False
  if request.method == 'POST':
    dba_id = request.form['dba_id']
    email = request.form['email']
    fname = request.form['fname']
    lname = request.form['lname']
    dob = request.form['dob']
    sex = request.form['sex']

    s = "INSERT INTO dba (dba_id, email, fname, lname, dob, sex) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(dba_id, email, fname, lname, dob, sex)
    g.conn.execute(s)

  sel_st = "SELECT dba_id, email, fname, lname, dob, sex FROM dba"

  results = []
  cursor = g.conn.execute(sel_st)

  for row in cursor:
      results.append(row)
  cursor.close()

  print results

  context = dict(data = results)

  return render_template('dba.html', isDBA=isDBA, **context)

@app.route('/game', methods=['GET', 'POST'])
def game():
  if request.method == 'POST':
    game_id = request.form['game_id']
    start_date = request.form['start_date']
    home_id = request.form['home_id']
    away_id = request.form['away_id']
    home_score = request.form['home_score']
    away_score = request.form['away_score']
    ref_id = request.form['ref_id']
    is_winner_home = request.form['is_winner_home']

    s = "INSERT INTO court (game_id, start_date, home_id, away_id, home_score, away_score, ref_id, is_winner_home) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(game_id, start_date, home_id, away_id, home_score, away_score, ref_id, is_winner_home)
    print s
    g.conn.execute(s)

  sel_st_dba = """
  SELECT game_id as "Game ID", start_date as "Start Date", home_id as "Home Team ID", away_id as "Away Team ID", home_score "Home Team Score", away_score as "Away Team Score", ref_id as "Referee ID", is_winner_home as "Is Winner Home?" FROM game
  """

  sel_st_user = '''
  SELECT G.start_date AS "Start Date", TH.name AS "Home Team", G.home_score AS "Home Score", TA.name "Away Team", G.away_score AS "Away Score", R.lname AS "Referee Name", G.is_winner_home AS "Did Home Team Win?"
  FROM Game G, Team TH, Team TA, Referee R
  WHERE G.home_id = TH.team_id AND G.away_id = TA.team_id AND G.ref_id = R.ref_id
  ORDER BY G.start_date
  '''

  cursor = g.conn.execute(sel_st_dba)
  results = []
  cursor = g.conn.execute(sel_st_dba)

  for row in cursor:
        results.append(row)
  cursor.close()

  print results

  cursor2 = g.conn.execute(sel_st_user)
  results2 = []
  cursor2 = g.conn.execute(sel_st_user)

  for row in cursor2:
        results2.append(row)
  cursor2.close()

  context = dict(data1=results, data2=results2)

  return render_template('game.html', isDBA=isDBA, **context)

@app.route('/player', methods=['GET', 'POST'])
def player():
  if request.method == 'POST':
    player_id = request.form['player_id']
    fname = request.form['fname']
    lname = request.form['lname']
    dob = request.form['dob']
    height = request.form['height']
    weight = request.form['weight']
    is_rhd = request.form['is_rhd']
    is_injured = request.form['is_injured']
    hometown = request.form['hometown']
    college = request.form['college']
    jersey_number = request.form['jersey_number']
    team_id = request.form['team_id']
    is_signed = request.form['is_signed']

    s = "INSERT INTO court (player_id, fname, lname, dob, height, weight, is_rhd, is_injured, hometown, college, jersey_number, team_id, is_signed) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(game_id, start_date, home_id, away_id, home_score, away_score, ref_id, is_winner_home)
    print s
    g.conn.execute(s)

  sel_st_dba = """
  SELECT player_id AS "Player ID", fname AS "First Name", lname AS "Last Name", dob AS "Date of Birth", height AS "Height", weight AS "Weight", is_rhd "Is Right-Handed?", is_injured AS "Is Injured?", hometown AS "Hometown", college AS "College", jersey_number AS "Jersey Number", team_id AS "Team ID", is_signed AS "Is Signed?" FROM player
  """
  #df_dba = pd.read_sql_query(sql=sel_st_dba, con=engine)

  sel_st_user = """
  SELECT P.fname AS "First Name", P.lname AS "Last Name", P.dob AS "Date of Birth", P.height AS "Height", P.weight AS "Weight", P.is_rhd "Is Right-Handed?", P.is_injured AS "Is Injured?", P.hometown AS "Hometown", P.college AS "College", jersey_number AS "Jersey Number", T.name AS "Team", P.is_signed AS "Is Signed?"
  FROM player P
  INNER JOIN Team T ON (P.team_id = T.team_id)
  """

  print isDBA

  cursor = g.conn.execute(sel_st_dba)
  results = []
  cursor = g.conn.execute(sel_st_dba)

  for row in cursor:
        results.append(row)
  cursor.close()

  cursor2 = g.conn.execute(sel_st_user)
  results2 = []
  cursor2 = g.conn.execute(sel_st_user)

  for row in cursor2:
        results2.append(row)
  cursor2.close()

  context = dict(data1= results, data2=results2)
  print context

  return render_template('player.html', isDBA=isDBA, **context)

@app.route('/search_player', methods=['GET','POST'])
def search_player():
  global isDBA
  if request.method == 'POST':
    fname = request.form['player_fname']
    lname = request.form['player_lname']

    sel_st = """
    SELECT player_id AS "Player ID", fname AS "First Name", lname AS "Last Name", dob AS "Date of Birth", height AS "Height", weight AS "Weight", is_rhd "Is Right-Handed?", is_injured AS "Is Injured?", hometown AS "Hometown", college AS "College", jersey_number AS "Jersey Number", team_id AS "Team ID", is_signed AS "Is Signed?"
    FROM player
    WHERE fname = '{}' AND lname = '{}'
    """.format(fname, lname)

  results = []
  cursor = g.conn.execute(sel_st)

  for row in cursor:
        results.append(row)
  cursor.close()

  print results

  context = dict(data = results)

  return render_template('search.html', isDBA=isDBA, **context)

@app.route('/plays_in', methods=['GET', 'POST'])
def plays_in():
  if request.method == 'POST':
    player_id = request.form['player_id']
    game_id = request.form['game_id']
    fg = request.form['fg']
    fga = request.form['fga']
    tp = request.form['tp']
    tpa = request.form['tpa']
    pts = request.form['pts']
    ast = request.form['ast']
    stl = request.form['stl']
    blk = request.form['blk']
    tov = request.form['tov']
    pf = request.form['pf']

    s = "INSERT INTO court (player_id, game_id, fg, fga, tp, tpa, pts, ast, stl, blk, tov, pf) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(player_id, game_id, fg, fga, tp, tpa, pts, ast, stl, blk, tov, pf)
    print s
    g.conn.execute(s)

  sel_st_dba = """
  SELECT PI.player_id as "Player ID", PI.game_id as "Game ID", PI.fg as "FG", PI.fga as "FGA", PI.tp as "TP", PI.tpa as "TPA", PI.pts as "PTS", PI.ast as "AST", PI.stl as "STL", PI.blk as "BLK", PI.tov as "TOV", PI.pf as "PF"
  FROM Plays_In PI
  """

  sel_st_user = """
  SELECT G.start_date as "Date", T.name as "Team", P.fname as "First Name", P.lname as "Last Name", PI.fg as "FG", PI.fga as "FGA", PI.tp as "TP", PI.tpa as "TPA", PI.pts as "PTS", PI.ast as "AST", PI.stl as "STL", PI.blk as "BLK", PI.tov as "TOV", PI.pf as "PF"
  FROM Plays_In PI
  INNER JOIN Player P ON (P.player_id = PI.player_id)
  INNER JOIN Team T ON (P.team_id = T.team_id)
  INNER JOIN Game G ON (G.game_id = PI.game_id)
  ORDER BY "Date"
  """

  print isDBA

  results = []
  cursor = g.conn.execute(sel_st_dba)

  for row in cursor:
      results.append(row)
  cursor.close()

  print results

  cursor2 = g.conn.execute(sel_st_user)
  results2 = []
  cursor2 = g.conn.execute(sel_st_user)

  for row in cursor2:
        results2.append(row)
  cursor2.close()

  context = dict(data1= results, data2=results2)

  return render_template('plays_in.html', isDBA=isDBA, **context)

@app.route('/referee', methods=['GET', 'POST'])
def referee():
  if request.method == 'POST':
    ref_id = request.form['ref_id']
    fname = request.form['fname']
    lname = request.form['lname']
    dob = request.form['dob']
    games_refereed['games_refereed']

    s = "INSERT INTO referee (ref_id, fname, lname, dob, games_refereed) VALUES ('{}', '{}', '{}', '{}', '{}')".format(game_id, start_date, home_id, away_id, home_score, away_score, ref_id, is_winner_home)
    print s
    g.conn.execute(s)

  sel_st = "SELECT ref_id, fname, lname, dob, games_refereed FROM referee"
  col_titles = ['Referee ID', 'First Name', 'Last Name', 'Date of Birth', 'Games Refereed']

  print isDBA

  results = []
  cursor = g.conn.execute(sel_st)

  for row in cursor:
        results.append(row)
  cursor.close()

  print results

  context = dict(data = results)

  return render_template('referee.html', isDBA=isDBA, **context)

@app.route('/team', methods=['GET', 'POST'])
def team():
  if request.method == 'POST':
    team_id = request.form['team_id']
    name = request.form['name']
    city = request.form['city']
    coach_id = request.form['coach']
    court_id = request.form['court_id']
    wins = request.form['wins']

    s = "INSERT INTO team (team_id, name, city, coach_id, court_id, wins, losses) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(team_id, name, city, coach_id, court_id, wins, losses)
    print s
    g.conn.execute(s)

  sel_st = "SELECT team_id, name, city, coach_id, court_id, wins, losses FROM team"
  col_titles = ['Team ID', 'Team Name', 'City', 'Coach ID', 'Court ID', 'Wins', 'Losses']

  results = []
  cursor = g.conn.execute(sel_st)

  for row in cursor:
        results.append(row)
  cursor.close()

  print results

  context = dict(data = results)

  return render_template('team.html', isDBA=isDBA, **context)

## Special Queries: ##

@app.route('/top-scoring-players', methods=['GET', 'POST'])
def top_scoring_players():
  global isDBA
  sel_st = """
  SELECT G.start_date AS "Game Date", T.name as "Team Name", P.fname as "First Name", P.lname AS "Last Name", PI.pts as "PTS",PI.fg as "FG", PI.fga as "FGA", PI.tp as "TP", PI.tpa as "TPA", PI.ast as "AST", PI.stl as "STL", PI.blk as "BLK", PI.tov as "TOV", PI.pf as "PF"
  FROM Player P
  INNER JOIN Team T ON (P.team_id = T.team_id)
  INNER JOIN Plays_In PI ON (P.player_id = PI.player_id)
  INNER JOIN Game G ON (G.game_id = PI.game_id)
  ORDER BY PI.pts DESC
  LIMIT 5
  """

  cursor = g.conn.execute(sel_st)
  results = []
  cursor = g.conn.execute(sel_st)

  for row in cursor:
        results.append(row)
  cursor.close()

  print results

  context = dict(data = results)

  return render_template('temp.html', isDBA=isDBA, **context)

@app.route('/three-point-kings', methods=['GET', 'POST'])
def three_point_kings():
  global isDBA
  sel_st = """
  SELECT G.start_date AS "Game Date", T.name as "Team Name", P.fname as "First Name", P.lname AS "Last Name", PI.pts as "PTS",PI.fg as "FG", PI.fga as "FGA", PI.tp as "TP", PI.tpa as "TPA", PI.ast as "AST", PI.stl as "STL", PI.blk as "BLK", PI.tov as "TOV", PI.pf as "PF"
  FROM Player P
  INNER JOIN Team T ON (P.team_id = T.team_id)
  INNER JOIN Plays_In PI ON (P.player_id = PI.player_id)
  INNER JOIN Game G ON (G.game_id = PI.game_id)
  ORDER BY PI.pts DESC
  WHERE
  LIMIT 5
  """

  cursor = g.conn.execute(sel_st)
  results = []
  cursor = g.conn.execute(sel_st)

  for row in cursor:
        results.append(row)
  cursor.close()

  print results

  context = dict(data = results)

  return render_template('top-scoring-players.html', isDBA=isDBA, **context)

@app.route('/injuries-on-teams', methods=['GET', 'POST'])
def injuries_on_teams():
  global isDBA
  sel_st = """
  SELECT COUNT(player.is_injured), team.name
  FROM team
  INNER JOIN player ON team.team_id = player.team_id
  GROUP BY team.name
  """

  cursor = g.conn.execute(sel_st)
  results = []
  cursor = g.conn.execute(sel_st)

  for row in cursor:
        results.append(row)
  cursor.close()

  print results

  context = dict(data = results)

  return render_template('injuries-on-teams.html', isDBA=isDBA, **context)

@app.route('/total-stats', methods=['GET', 'POST'])
def total_stats():
  global isDBA
  sel_st = """
  SELECT T.name as "Team", P.fname as "First Name", P.lname as "Last Name", SUM(PI.fg) as "FG", SUM(PI.fga) as "FGA", SUM(PI.tp) as "TP", SUM(PI.tpa) as "TPA", SUM(PI.pts) as "PTS", SUM(PI.ast) as "AST", SUM(PI.stl) as "STL", SUM(PI.blk) as "BLK", SUM(PI.tov) as "TOV", SUM(PI.pf) as "PF"
  FROM Plays_In PI
  INNER JOIN Player P ON (P.player_id = PI.player_id)
  INNER JOIN Team T ON (P.team_id = T.team_id)
  INNER JOIN Game G ON (G.game_id = PI.game_id)
  GROUP BY "Team", "First Name", "Last Name"
  ORDER BY "Team"
  """

  cursor = g.conn.execute(sel_st)
  results = []
  cursor = g.conn.execute(sel_st)

  for row in cursor:
        results.append(row)
  cursor.close()

  print results

  context = dict(data = results)

  return render_template('total-stats.html', isDBA=isDBA, **context)

@app.route('/avg-stats', methods=['GET', 'POST'])
def avg_stats():
  global isDBA
  sel_st = """
  SELECT T.name as "Team", P.fname as "First Name", P.lname as "Last Name", avg(PI.fg) as "FG", avg(PI.fga) as "FGA", AVG(PI.tp) as "TP", AVG(PI.tpa) as "TPA", AVG(PI.pts) as "PTS", AVG(PI.ast) as "AST", AVG(PI.stl) as "STL", AVG(PI.blk) as "BLK", AVG(PI.tov) as "TOV", AVG(PI.pf) as "PF"
  FROM Plays_In PI
  INNER JOIN Player P ON (P.player_id = PI.player_id)
  INNER JOIN Team T ON (P.team_id = T.team_id)
  INNER JOIN Game G ON (G.game_id = PI.game_id)
  GROUP BY "Team", "First Name", "Last Name"
  ORDER BY "Team"
  """

  cursor = g.conn.execute(sel_st)
  results = []
  cursor = g.conn.execute(sel_st)

  for row in cursor:
        results.append(row)
  cursor.close()

  print results

  context = dict(data = results)

  return render_template('total-stats.html', isDBA=isDBA, **context)
if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
