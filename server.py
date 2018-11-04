from jinja2 import StrictUndefined
import json
from flask import Flask, render_template, redirect, request, flash, session, url_for, jsonify, flash
from flask_debugtoolbar import DebugToolbarExtension
import requests
import os

from model import Company, Industry, Interest, Salary, connect_to_db, db
from forms import CompanyForm
from job_listings_scraper import get_job_listings


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"


# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route("/search")
def select_company():
    """Select Company for search."""

    form = CompanyForm()

    return render_template("company_search_form.html", form=form)

@app.route("/companies")
def companydic():
    """Using for Jquery company name Autocomplete."""

    res = Company.query.all()
    list_companies = [r.as_dict() for r in res]
    return jsonify(list_companies)    


@app.route("/company_view")
def create_result_view():
    """Create the company's salary table."""

    from datetime import datetime; start = datetime.now()
    form = CompanyForm(request.args)
    company_name = form.company.data
    company_name = company_name.upper()
    company = Company.query.options(
        db.joinedload("industry")
          .joinedload("companies")
          .joinedload("interest")
    ).filter_by(name=company_name).first()
    print('#' * 20, datetime.now() - start) # for checking runtime
    
    job_listings = get_job_listings(company_name)
    print('#' * 20, datetime.now() - start) # for checking runtime


    company_infos = get_company_infos(company_name)
    print('#' * 20, datetime.now() - start) # for checking runtime

    interest_chart=create_interest_chart(company)

    if company.industry:
        ranking = get_interest_growth_ranking(company)
        industry_name = company.industry.name
    
    else:
        ranking = None
        industry_name = None


    if company != None:

        salary_query = company.salaries

        return render_template("form.html", salary_query=salary_query, 
                                company_name=company_name, job_listings=job_listings,
                                ranking =ranking, industry_name=industry_name, 
                                company_infos=company_infos,
                                interest_chart=interest_chart)

    else:

        flash("Please check the company name.")
        return redirect("/search")


def create_interest_chart(company):
    """Google trends interest chart generator."""

    if not company.interest:
        return None

    else:

        chart_dic = { 
                      "label1": [ obj.date.isoformat() for obj in company.interest ],
                      "label2": [ obj.interest for obj in company.interest ]
                    }
              
        return chart_dic


def get_interest_growth(company):
    """Get the interest ranking in the same industy companies."""

    interest = sorted(company.interest, key=lambda x: x.date)

    interest_start = interest[0]
    interest_end = interest[-1]

    # preventing for division by zero error.
    if interest_start.interest == 0:
        interest_growth = (interest_end.interest - 1) / 1 * 100
        
    else:
        interest_growth = (interest_end.interest - interest_start.interest) / interest_start.interest * 100

    return interest_growth


def get_interest_growth_ranking(target_company):

    larger = []
    target_interest_growth = get_interest_growth(target_company)

    for company in target_company.industry.companies:

        if company.interest:
            company_interest_growth = get_interest_growth(company)
            if company_interest_growth > target_interest_growth:
                larger.append(company_interest_growth)
            else:
                continue
        else:
            continue


    ranking = len(larger) + 1
    total = len(target_company.industry.companies)

    return ranking, total



def get_company_infos(company_name):
    """Get Company's desc and logo img using Bing API."""

    subscription_key = os.environ['BING_KEY'] # error occurs
    assert subscription_key

    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
    search_term = company_name.lower()+" company profile"

    headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
    params  = {"q": search_term, "textDecorations":True, "textFormat":"HTML"}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    if search_results:

        company_desc = search_results['entities']['value'][0]['description']
        company_img = search_results['entities']['value'][0]['image']['thumbnailUrl']

        return (company_desc, company_img)

    else:

        return (None, None)


@app.route("/news.json")
def get_news():
    """Get news for specific date, 
    when user click the interest chart's specific point."""
    
    news_key = os.environ['NEWS_KEY']

    company_name2 = request.args.get("company_name")
    company_name = company_name2.lower()

    news_date2 = request.args.get("from")
    news_date = news_date2[:10]


    print(news_date)

    url = "https://newsapi.org/v2/everything"
    
    params  = { 
            "q": company_name, 
            "from": news_date,    
            "to": news_date,
            "sortBy" : "popularity",
            "apiKey" : news_key
            }

    response = requests.get(url, params=params)
    print(response.url)

    return jsonify(response.json()['articles'][0])



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)
    # db.create_all()

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')