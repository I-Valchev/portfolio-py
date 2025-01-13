from rich.console import Console
from rich.table import Table
import os
import yaml
import questionary
from datetime import datetime

data_folder = "data"
console = Console()

def list_folders(path):
    return [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

def load_config(portfolio):
    config_path = os.path.join(data_folder, portfolio, "config.yaml")
    with open(config_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)

def list_transactions_or_valuations(portfolio, platform, category):
    file_path = os.path.join(data_folder, portfolio, f"{platform}-{category}.txt")
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r", encoding="utf-8") as file:
        return file.readlines()

def append_transaction_or_valuation(portfolio, platform, category, date, amount):
    file_path = os.path.join(data_folder, portfolio, f"{platform}-{category}.txt")
    with open(file_path, "a+", encoding="utf-8") as file:
        file.seek(0, os.SEEK_END)
        if file.tell() > 0:
            file.seek(file.tell() - 1)
            if file.read(1) != "\n":
                file.write("\n")
        file.write(f"{date} {amount}\n")

def display_entries(portfolio, platform, category):
    entries = list_transactions_or_valuations(portfolio, platform, category)
    if entries:
        table = Table(title=f"{platform.capitalize()} {category.capitalize()}")
        table.add_column("Date", style="cyan")
        table.add_column("Amount", style="green")
        for entry in entries:
            date, amount = entry.strip().split(" ", 1)
            table.add_row(date, amount)
        console.print(table)
    else:
        console.print("[yellow]No records found.[/yellow]")

def select_option(prompt, choices):
    return questionary.select(prompt, choices=choices).ask()

def add_entry(portfolio, platform, category):
    date = questionary.text("Enter transaction date (default: today)", default=datetime.today().strftime("%d.%m.%Y")).ask()
    amount = questionary.text("Enter transaction amount").ask()
    if date and amount:
        append_transaction_or_valuation(portfolio, platform, category, date, amount)
        console.print("[green]Entry added successfully![/green]")

def main():
    console.print("[bold cyan]Stock Portfolio Manager[/bold cyan]")
    portfolio, category, platform = None, None, None
    
    while True:
        if not portfolio:
            portfolio = select_option("Select portfolio", list_folders(data_folder) + ["Go Back"])
            if portfolio == "Go Back":
                continue
        
        if not category:
            category = select_option("Choose category", ["valuations", "transactions", "Go Back"])
            if category == "Go Back":
                portfolio = None
                continue
        
        if not platform:
            config = load_config(portfolio)
            platforms = config.get("platforms", {})
            platform_choices = [(platforms[key]["pretty"], key) for key in platforms]
            platform_pretty = select_option("Select platform", [p[0] for p in platform_choices] + ["Go Back"])
            if platform_pretty == "Go Back":
                category = None
                continue
            platform = next(key for pretty, key in platform_choices if pretty == platform_pretty)
        
        display_entries(portfolio, platform, category)
        action = select_option("Choose action", ["add", "Go Back", "cancel"])
        
        if action == "Go Back":
            platform = None
            continue
        if action == "cancel":
            console.print("[bold red]Operation canceled.[/bold red]")
            return
        
        add_entry(portfolio, platform, category)
        return

if __name__ == "__main__":
    main()
