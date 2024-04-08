import requests
from bs4 import BeautifulSoup as bs
from markupsafe import escape
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import pytz
import random

app = Flask(__name__)
cors = CORS(app, resources={
    r"/score/*": {"origins": [r'^https://.+sanweb.info$', r'^https://.+mskian.com$']}
})
user_agent_list = [
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0'
]
get_random_agent = random.choice(user_agent_list)

headers = {
    'User-Agent': get_random_agent,
    'Cache-Control': 'no-cache'
}

@app.route('/')
def hello():
    return jsonify({'Code': 200, 'message': 'Python - Free Cricket Score API - JSON'})

@app.route('/score', methods=['GET'])
def score():
    get_id = escape(request.args.get('id'))
    if get_id:
        session_object = requests.Session()
        r = session_object.get('https://www.cricbuzz.com/live-cricket-scores/' + get_id, headers=headers)
        soup = bs(r.content, 'lxml')
        data = {}
        status = 'Match Stats will Update Soon...'
        for cls, key in [
            ("cb-col-100 cb-min-stts cb-text-complete", "update"),
            ("cb-text-inprogress", "update"),
            ("cb-col cb-col-100 cb-font-18 cb-toss-sts cb-text-abandon", "update"),
            ("cb-text-stumps", "update"),
            ("cb-text-lunch", "update"),
            ("cb-text-inningsbreak", "update"),
            ("cb-text-tea", "update"),
            ("cb-text-rain", "update"),
            ("cb-text-wetoutfield", "update"),
            ("cb-col-50", "batter_one"),
            ("cb-col-50", "batter_two"),
            ("cb-col-10 ab text-right", "batter_one_run"),
            ("cb-col-10 ab text-right", "batter_two_run"),
            ("cb-col-10 ab text-right", "batter_one_ball"),
            ("cb-col-10 ab text-right", "batter_two_ball"),
            ("cb-col-14 ab text-right", "batter_one_sr"),
            ("cb-col-14 ab text-right", "batter_two_sr"),
            ("cb-col-50", "bowler_one"),
            ("cb-col-50", "bowler_two"),
            ("cb-col-10 text-right", "bowler_one_over"),
            ("cb-col-10 text-right", "bowler_two_over"),
            ("cb-col-10 text-right", "bowler_one_run"),
            ("cb-col-10 text-right", "bowler_two_run"),
            ("cb-col-14 text-right", "bowler_one_eco"),
            ("cb-col-14 text-right", "bowler_two_eco"),
            ("cb-col-8 text-right", "bowler_one_wicket"),
            ("cb-col-8 text-right", "bowler_two_wicket")
        ]:
            elements = soup.find_all("div", attrs={"class": cls})
            if elements:
                data[key] = elements[0].text.strip()
                status = data[key]
            else:
                data[key] = 'Match Stats will Update Soon'
        if "startDate" in soup.find("span", itemprop="startDate").attrs:
            match_date = soup.find("span", itemprop="startDate").attrs["content"]
            match_date = datetime.strptime(match_date.split('+')[0], "%Y-%m-%dT%H:%M:%S").astimezone(pytz.timezone("Asia/Kolkata")).strftime("Date: %Y-%m-%d - Time: %I:%M:%S %p (Indian Local Time)")
        else:
            match_date = 'Match Stats will Update Soon'
        data["match_date"] = match_date
        return jsonify(data)
    else:
        return jsonify({
            'title': 'Data not Found',
            'update': 'Data not Found',
            'livescore': 'Data not Found',
            'runrate': 'Data not Found',
            'batter_one': 'Data not Found',
            'batter_one_run': 'Data not Found',
            'batter_one_ball': 'Data not Found',
            'batter_one_sr': 'Data not Found',
            'batter_two': 'Data not Found',
            'batter_two_run': 'Data not Found',
            'batter_two_ball': 'Data not Found',
            'batter_two_sr': 'Data not Found',
            'bowler_one': 'Data not Found',
            "bowler_one_over": 'Data not Found',
            "bowler_one_run": 'Data not Found',
            "bowler_one_wicket": 'Data not Found',
            "bowler_one_eco": 'Data not Found',
            'bowler_two': 'Data not Found',
            "bowler_two_over": 'Data not Found',
            "bowler_two_run": 'Data not Found',
            "bowler_two_wicket": 'Data not Found',
            "bowler_two_eco": 'Data not Found'
        })

if __name__ == "__main__":
    app.run()





headers = {
    'User-Agent': 'Your User Agent',
}

def get_live_score(id):
    session_object = requests.Session()
    r = session_object.get(f'https://www.cricbuzz.com/live-cricket-scores/{id}', headers=headers)
    soup = bs(r.content, 'lxml')

    try:
        status_elements = [
            soup.find_all("div", attrs={"class": "cb-col cb-col-100 cb-min-stts cb-text-complete"}),
            soup.find_all("div", attrs={"class": "cb-text-inprogress"}),
            soup.find_all("div", attrs={"class": "cb-col cb-col-100 cb-font-18 cb-toss-sts cb-text-abandon"}),
            soup.find_all("div", attrs={"class": "cb-text-stumps"}),
            soup.find_all("div", attrs={"class": "cb-text-lunch"}),
            soup.find_all("div", attrs={"class": "cb-text-inningsbreak"}),
            soup.find_all("div", attrs={"class": "cb-text-tea"}),
            soup.find_all("div", attrs={"class": "cb-text-rain"}),
            soup.find_all("div", attrs={"class": "cb-text-wetoutfield"})
        ]
        status = next((element[0].text.strip() for element in status_elements if element), 'Match Stats will Update Soon')
        match_date_element = soup.find('span', itemprop='startDate')
        match_date = 'Match Stats will Update Soon'
        if match_date_element:
            match_time = match_date_element.get('content')
            new_dt = match_time.split('+')[0]
            utc_time = datetime.strptime(new_dt, "%Y-%m-%dT%H:%M:%S")
            utc_time_utc = utc_time.replace(tzinfo=pytz.UTC)
            target_timezone = pytz.timezone("Asia/Kolkata")
            local_time = utc_time_utc.astimezone(target_timezone)
            match_date = local_time.strftime("Date: %Y-%m-%d - Time: %I:%M:%S %p (Indian Local Time)")
        
        live_score = soup.find("span", attrs={"class": "cb-font-20 text-bold"}).text.strip() if soup.find("span", attrs={"class": "cb-font-20 text-bold"}) else 'Data Not Found'
        title = soup.find("h1", attrs={"class": "cb-nav-hdr cb-font-18 line-ht24"}).text.strip().replace(", Commentary", "") if soup.find("h1", attrs={"class": "cb-nav-hdr cb-font-18 line-ht24"}) else 'Data Not Found'
        run_rate = soup.find("span", attrs={"class": "cb-font-12 cb-text-gray"}).text.strip().replace("CRR:\u00a0", "") if soup.find("span", attrs={"class": "cb-font-12 cb-text-gray"}) else 'Data Not Found'
        batter_elements = soup.find_all("div", attrs={"class": "cb-col cb-col-50"})
        batter_one = batter_elements[1].text.strip() if batter_elements else 'Data Not Found'
        batter_two = batter_elements[2].text.strip() if len(batter_elements) > 2 else 'Data Not Found'
        batter_stats_elements = soup.find_all("div", attrs={"class": "cb-col cb-col-10 ab text-right"})
        batter_one_run = batter_stats_elements[0].text.strip() if batter_stats_elements else 'Data Not Found'
        batter_two_run = batter_stats_elements[2].text.strip() if len(batter_stats_elements) > 2 else 'Data Not Found'
        batter_one_ball = batter_stats_elements[1].text.strip() if batter_stats_elements else 'Data Not Found'
        batter_two_ball = batter_stats_elements[3].text.strip() if len(batter_stats_elements) > 3 else 'Data Not Found'
        batter_sr_elements = soup.find_all("div", attrs={"class": "cb-col cb-col-14 ab text-right"})
        batter_one_sr = batter_sr_elements[0].text.strip() if batter_sr_elements else 'Data Not Found'
        batter_two_sr = batter_sr_elements[1].text.strip() if len(batter_sr_elements) > 1 else 'Data Not Found'
        bowler_elements = soup.find_all("div", attrs={"class": "cb-col cb-col-50"})
        bowler_one = bowler_elements[4].text.strip() if bowler_elements else 'Data Not Found'
        bowler_two = bowler_elements[5].text.strip() if len(bowler_elements) > 5 else 'Data Not Found'
        bowler_stats_elements = soup.find_all("div", attrs={"class": "cb-col cb-col-10 text-right"})
        bowler_one_over = bowler_stats_elements[4].text.strip() if bowler_stats_elements else 'Data Not Found'
        bowler_two_over = bowler_stats_elements[6].text.strip() if len(bowler_stats_elements) > 6 else 'Data Not Found'
        bowler_one_run = bowler_stats_elements[5].text.strip() if bowler_stats_elements else 'Data Not Found'
        bowler_two_run = bowler_stats_elements[7].text.strip() if len(bowler_stats_elements) > 7 else 'Data Not Found'
        bowler_eco_elements = soup.find_all("div", attrs={"class": "cb-col cb-col-14 text-right"})
        bowler_one_eco = bowler_eco_elements[2].text.strip() if bowler_eco_elements else 'Data Not Found'
        bowler_two_eco = bowler_eco_elements[3].text.strip() if len(bowler_eco_elements) > 3 else 'Data Not Found'
        bowler_wicket_elements = soup.find_all("div", attrs={"class": "cb-col cb-col-8 text-right"})
        bowler_one_wicket = bowler_wicket_elements[5].text.strip() if bowler_wicket_elements else 'Data Not Found'
        bowler_two_wicket = bowler_wicket_elements[7].text.strip() if len(bowler_wicket_elements) > 7 else 'Data Not Found'
    except IndexError:
        status = 'Match Stats will Update Soon...'
        match_date = 'Match Stats will Update Soon...'
        live_score = 'Data Not Found'
        title = 'Data Not Found'
        run_rate = 'Data Not Found'
        batter_one = 'Data Not Found'
        batter_two = 'Data Not Found'
        batter_one_run = 'Data Not Found'
        batter_two_run = 'Data Not Found'
        batter_one_ball = 'Data Not Found'
        batter_two_ball = 'Data Not Found'
        batter_one_sr = 'Data Not Found'
        batter_two_sr = 'Data Not Found'
        bowler_one = 'Data Not Found'
        bowler_two = 'Data Not Found'
        bowler_one_over = 'Data Not Found'
        bowler_two_over = 'Data Not Found'
        bowler_one_run = 'Data Not Found'
        bowler_two_run = 'Data Not Found'
        bowler_one_eco = 'Data Not Found'
        bowler_two_eco = 'Data Not Found'
        bowler_one_wicket = 'Data Not Found'
        bowler_two_wicket = 'Data Not Found'

    return {
        "success": True,
        "livescore": {
            'title': title,
            'update': status,
            'current': live_score,
            'runrate': f'CRR: {run_rate}',
            'batsman': batter_one,
            'batsmanrun': batter_one_run,
            'ballsfaced': f'({batter_one_ball})',
            'sr': batter_one_sr,
            'batsmantwo': batter_two,
            'batsmantworun': batter_two_run,
            'batsmantwoballfaced':  f'({batter_two_ball})',
            'batsmantwosr': batter_two_sr,
            'bowler': bowler_one,
            "bowlerover": bowler_one_over,
            "bowlerruns": bowler_one_run,
            "bowlerwickets": bowler_one_wicket,
            "bowlereconomy": bowler_one_eco,
            'bowlertwo': bowler_two,
            "bowlertwoover": bowler_two_over,
            "bowlertworuns": bowler_two_run,
            "bowlertwowickets": bowler_two_wicket,
            "bowlertwoeconomy": bowler_two_eco
        }
    }



@app.route('/score/live', methods=['GET'])
def live():
    id = request.args.get('id')
    if id:
        return jsonify(get_live_score(id))
    else:
        return jsonify({
            "success": False,
            "livescore": {
                'title': 'Data not Found',
                'update': 'Data not Found',
                'current': 'Data not Found',
                'runrate': 'Data not Found',
                'batsman': 'Data not Found',
                'batsmanrun': 'Data not Found',
                'ballsfaced': 'Data not Found',
                'sr': 'Data not Found',
                'batsmantwo': 'Data not Found',
                'batsmantworun': 'Data not Found',
                'batsmantwoballfaced': 'Data not Found',
                'batsmantwosr': 'Data not Found',
                'bowler': 'Data not Found',
                "bowlerover": 'Data not Found',
                "bowlerruns": 'Data not Found',
                "bowlerwickets": 'Data not Found',
                "bowlereconomy": 'Data not Found',
                'bowlertwo': 'Data not Found',
                "bowlertwoover": 'Data not Found',
                "bowlertworuns": 'Data not Found',
                "bowlertwowickets": 'Data not Found',
                "bowlertwoeconomy": 'Data not Found'
            }
        })



@app.errorhandler(404)
def invalid_route(e):
    return jsonify({
        'title': 'Data not Found',
        'update': 'Data not Found',
        'livescore': 'Data not Found',
        'runrate': 'Data not Found',
        'batterone': 'Data not Found',
        'batsmanonerun': 'Data not Found',
        'batsmanoneball': 'Data not Found',
        'batsmanonesr': 'Data not Found',
        'battertwo': 'Data not Found',
        'batsmantworun': 'Data not Found',
        'batsmantwoball': 'Data not Found',
        'batsmantwosr': 'Data not Found',
        'bowlerone': 'Data not Found',
        "bowleroneover": 'Data not Found',
        "bowleronerun": 'Data not Found',
        "bowleronewickets": 'Data not Found',
        "bowleroneeconomy": 'Data not Found',
        'bowlertwo': 'Data not Found',
        "bowlertwoover": 'Data not Found',
        "bowlertworun": 'Data not Found',
        "bowlertwowickets": 'Data not Found',
        "bowlertwoeconomy": 'Data not Found',
    })

from flask import Flask, jsonify

app = Flask(__name__)

@app.errorhandler(500)
def handle_server_error(e):
    return jsonify({
        'title': 'Internal Server Error',
        'message': 'Something went wrong on the server.'
    }), 500

if __name__ == '__main__':
    app.run()


