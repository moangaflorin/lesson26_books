import gradio as gr
import books_db_actions as db
from init_config import config
import os
import pandas as pd

def get_books(user_input):

    if user_input:

        query = f"""
                select a."name", b."name", b.number_of_sales, b.reviews from authors a
                join books b on a.author_id = b.author_id
                where a."name" = '{user_input}'
                order by b.number_of_sales desc;"""
        response = db.get_data(query, database_config)
        df = pd.DataFrame(response)
        if df.empty:
            return df
        else:
            raise Exception("Author was not found...")
    else:
        print("You need to insert an author")
        raise Exception("You need to insert an author")

def add_book(name, sales, review, author):
    if name and sales and review and author:
        if not sales.isnumeric():

            raise Exception("Sales parameter must be a number")
        if not review.isnumeric():
            raise Exception("Review parameter must be a number")
        if author.isnumeric():
            raise Exception("Author parameter must be a string")

        if int(sales) <= 0:
            raise Exception("Sales must be greater than 0")
        author_name = db.get_data(f"""select author_id from punlic.authors a where "name" = '{author}' limit 1;""", database_config)
        if len(author_name) > 0:
            author_id = author_name[0]['author_id']
            db.insert_row(f"""insert into books(\"name\", number_of_sales, reviews, author_id) values ('{name}', {int(sales)}, {int(review)}, {author_id});""",
                          database_config)
        else:

            raise Exception("Author was not found in the database ")
    else:
        raise Exception("All values are mandatory")

def delete_book(name):
    if name:
        db.delete_row(name, database_config)
    else:
        raise Exception("Book name is mandatory for deletion")


def start_gui_app():
    with gr.Blocks() as app:
        with gr.Row():
            with gr.Column(scale=1):
                text_input = gr.Textbox(label="Write an author")
            with gr.Column(scale=1):
                get_books_button = gr.Button("Show Books")
        with gr.Row():
            response_table = gr.Dataframe(label="Results")
            get_books_button.click(fn=get_books, inputs=text_input, outputs=response_table)
        with gr.Row():
            with gr.Column(scale=1):
                new_book = gr.Textbox(label="New Book")
            with gr.Column(scale=1):
                number_of_sales = gr.Textbox(label="Sales")
            with gr.Column(scale=1):
                reviews = gr.Textbox(label="Review")
            with gr.Column(scale=1):
                author = gr.Textbox(label="Author Name")
        with gr.Row():
            add_book_btn =  gr.Button("Add Book")
            add_book_btn.click(fn=add_book, inputs=[new_book, number_of_sales, reviews, author])
        with gr.Row():
            with gr.Column(scale=1):
                delete_book_input = gr.Textbox(label="Delete book")
                delete_book_btn = gr.Button("Delete")
                delete_book_btn.click(fn=delete_book, inputs=delete_book_input)

            with gr.Column(scale=2):
                pass
    app.launch(show_error=True)

if __name__ == '__main__':
    database_config = config.get("database_config")
    database_config['password'] = os.environ['db_password']
    start_gui_app()