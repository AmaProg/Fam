from typer import Typer

app = Typer(help="Allows you to manage invoices.")

invoice_command: dict = {"app": app, "name": "invoice"}


@app.command(help="Allows you to define the amounts needed to pay invoices.")
def payment():
    pass
