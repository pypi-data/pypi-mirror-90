#!/usr/bin/env python

import click
# import ujson
from .. import utils
from .. import remote
from decimal import Decimal
import itertools
import pandas as pd
pd.options.display.float_format = '{:,}'.format


def positions_list(options):

    options["is_positions"] = True

    data, errors = trades_list(options)

    table_data = []
    for row in data:
        del row['closed_at']
        del row['min_qty']
        del row['max_qty']
        table_data.append(row)
    click.echo(utils.to_table(table_data))

    """

    account = options.first("account")
    # accounts_data, errors = remote.api.get("/accounts")
    # accounts = {k: v["name"] for k, v in accounts_data.items()}
    # if account not in accounts:
    #     click.echo(f"Account `{account}` doesn't exist or was deleted.")
    #     return

    endpoint = "/positions"
    payload = {}

    if account:
        endpoint = "/account/{account}/positions".format(account=account)
    if options.get("strategy"):
        payload["strategies"] = options.get("strategy")
    if options.get("start"):
        payload["date_from"] = options.get("start")
    if options.get("end"):
        payload["date_to"] = options.get("end")
    if options.get("status"):
        payload["statuses"] = options.get("status")

    if payload:
        data, errors = remote.api.get(endpoint, json=payload)
    else:
        data, errors = remote.api.get(endpoint)

    if options.get("raw"):
        if not data:
            click.echo("\n[]")
        else:
            click.echo(utils.to_json(data, errors))
        return

    if not data:
        click.echo("\nNo positions found.")
        return

    table_data = []

    if not account:
        # display count
        for act, positions in data.items():
            table_data.append({
                "account": act,  # accounts.get(act, act),
                "positions": len(positions)
            })
    else:
        # display  order list
        if not data.get(account):
            click.echo("\nNo positions found for account {}".format(account))
            return

        for item in data.get(account):
            table_data.append({
                "id": item["order_id"],
                "asset": item["ticker"],
                "side": item["side"],
                "qty": "{:,.0f}".format(Decimal(item["qty"])),
                "filled_qty": "{:,.0f}".format(Decimal(item["filled_qty"])),
                "avg_fill_price": item["avg_fill_price"],
                "status": item["status"]
            })
    click.echo(utils.to_table(table_data))
    """

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def trades_list(options):

    def read_trades(trades, account=None):
        last_prices = {}
        rows = []
        for item in trades:
            row = {
                "asset": item["ticker"],
                "side": item["side"],
                "strategy": item["strategy"],
                "account": None,
                "opened_at": None,
                "closed_at": item["closed_at"],
                "max_qty": "{:,.0f}".format(Decimal(item["max_qty"])),
                "min_qty": "{:,.0f}".format(Decimal(item["min_qty"])),
                "avg_qty": "{:,.0f}".format(Decimal(item["avg_qty"])),
                "avg_buy_price": item["avg_buy_price"],
                "avg_sell_price": item["avg_sell_price"],
                "currency": item["currency"],
                "pnl": item["pnl"],
                "pnl_%": item["pnl_pct"],
            }
            if account:
                row["account"] = account
            else:
                del row["account"]

            if item.get("opened_at"):
                row["opened_at"] = item["opened_at"]
            else:
                del row["opened_at"]

            if not row["avg_buy_price"]:
                if not last_prices.get(row["asset"]):
                    last_prices[row["asset"]] = remote.api.get(f'/pricing/last/{row["asset"]}:{item["country"]}')[0].get("price")
                if last_prices.get(row["asset"]):
                    row["avg_buy_price"] = last_prices.get(row["asset"])
            if not row["avg_sell_price"]:
                if not last_prices.get(row["asset"]):
                    last_prices[row["asset"]] = remote.api.get(f'/pricing/last/{row["asset"]}:{item["country"]}')[0].get("price")
                if last_prices.get(row["asset"]):
                    row["avg_sell_price"] = last_prices.get(row["asset"])

            if row["avg_buy_price"] and row["avg_sell_price"]:
                row['pnl'] = float(row["avg_sell_price"]) - float(row["avg_buy_price"])
                row['pnl_%'] = float(row["avg_sell_price"]) / float(row["avg_buy_price"]) - 1
                if row["side"] == "short":
                    row['pnl'] = float(row["avg_buy_price"]) - float(row["avg_sell_price"])
                    row['pnl_%'] = float(row["avg_buy_price"]) / float(row["avg_sell_price"]) - 1

                row['pnl'] = "{:,.2f}".format(Decimal(row['pnl'] * float(row["avg_qty"])))
                row['pnl_%'] *= float(row["avg_qty"]) * 100
                row['pnl_%'] = "{:,.2f}".format(Decimal(row['pnl_%']))
                row['avg_buy_price'] = "{:,.2f}".format(Decimal(row['avg_buy_price']))
                row['avg_sell_price'] = "{:,.2f}".format(Decimal(row['avg_sell_price']))

            rows.append(row)
        return rows

    account = options.first("account")
    # accounts_data, errors = remote.api.get("/accounts")
    # accounts = {k: v["name"] for k, v in accounts_data.items()}
    # if account not in accounts:
    #     click.echo(f"Account `{account}` doesn't exist or was deleted.")
    #     return

    endpoint = "/trades"
    payload = {}

    if account:
        endpoint = "/account/{account}/trades".format(account=account)
    if options.get("strategy"):
        payload["strategies"] = options.get("strategy")
    if options.get("start"):
        payload["date_from"] = options.get("start")
    if options.get("end"):
        payload["date_to"] = options.get("end")
    if options.get("status"):
        payload["statuses"] = options.get("status")

    if payload:
        data, errors = remote.api.get(endpoint, json=payload)
    else:
        data, errors = remote.api.get(endpoint)

    if options.get("raw"):
        if not data:
            click.echo("\n[]")
        else:
            click.echo(utils.to_json(data, errors))
        click.exit()

    if not data:
        if options.first("is_positions", False):
            click.echo("\nNo positions found.")
        else:
            click.echo("\nNo trades found.")
        click.exit()

    # display  order list
    if not data:
        if options.first("is_positions", False):
            click.echo("\nNo positions found for account {}".format(account))
        else:
            click.echo("\nNo trades found for account {}".format(account))
        click.exit()

    table_data = {
        "all": [],
        "opened": [],
        "closed": []
    }

    if options.first("strategy"):
        rows = []
        for account, account_data in data.items():
            rows.append(read_trades(account_data, account))
        rows = list(itertools.chain.from_iterable(rows))
    else:
        rows = read_trades(data)

    for row in rows:
        if options.first("strategy"):
            del row["strategy"]
        table_data["all"].append(row)
        if row["closed_at"]:
            table_data["closed"].append(row)
        else:
            table_data["opened"].append(row)

    if options.first("is_positions", False):
        return table_data["opened"], errors

    click.echo(utils.to_table(table_data["all"]))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


