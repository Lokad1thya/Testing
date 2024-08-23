from flask import Flask, render_template, request, redirect, url_for
from nike import search_nike_products
from superkicks import search_superkicks_products
from vegNonVeg import search_vegnonveg_products

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()
        if search_query:
            return redirect(url_for('search_results', query=search_query))
    return render_template('index.html')

@app.route('/search_results', methods=['GET'])
def search_results():
    query = request.args.get('query', '')
    if query:
        # Perform search on multiple sites
        results_superkicks = search_superkicks_products(query)
        results_vegnonveg = search_vegnonveg_products(query)
        results_nike = search_nike_products(query)

        return render_template('results.html', 
                               query=query,
                               results_superkicks=results_superkicks,
                               results_vegnonveg=results_vegnonveg,
                               results_nike=results_nike)
    return render_template('results.html', query=query,
                           results_superkicks=[], results_vegnonveg=[], results_nike=[])

if __name__ == '__main__':
    app.run(debug=False)
