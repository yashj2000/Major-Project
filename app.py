from flask import Flask,render_template,request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
bookFinal = pickle.load(open('bookFinal.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(bookFinal['Book-Title'].values),
                           author=list(bookFinal['Book-Author'].values),
                           image=list(bookFinal['Image-URL-M'].values),
                           votes=list(bookFinal['num_ratings'].values),
                           rating=[round(r, 2) for r in bookFinal['avg_ratings'].values]
                           )
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    #try catch
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]


    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html',data=data)

@app.route('/popular')
def popular_ui():
    return render_template('popular.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=[round(r, 2) for r in popular_df['avg_ratings'].values]
                           )

@app.route('/summary', methods=['GET'])
def book_summary():
    # Get the book title from the query parameters
    book_title = request.args.get('title')

    # Search for the book in the DataFrame
    book = books.loc[books['Book-Title'] == book_title]

    # Check if the book is found
    if book.empty:
        # Handle the case when the book is not found
        return "Book not found."

    # Fetch the clean_summary for the book
    summary = book.iloc[0]['clean_summary']

    Bimg = book.iloc[0]['Image-URL-M']

    return render_template('summary.html', book_title=book_title, summary=summary,Bimg=Bimg)


if __name__ == '__main__':
    app.run(debug=True)