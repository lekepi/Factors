from models import session, FactorMarketData, FactorPosition, Position, Product
from datetime import date


def download_factor_position():
    today = date.today()
    session.query(FactorPosition).filter(FactorPosition.entry_date == today).delete()
    session.commit()

    factor_md_list = session.query(FactorMarketData).filter(FactorMarketData.entry_date == today).all()
    position_list = session.query(Position).filter(Position.entry_date == today).all()

    factor_position_list = []

    for position in position_list:

        product_id = position.product_id
        notional_usd = position.mkt_value_usd
        parent_fund_id = position.parent_fund_id

        factor_md_matches = [f for f in factor_md_list if f.ticker == position.product.ticker]
        for factor_md in factor_md_matches:
            coeff = factor_md.coeff
            factor_id = factor_md.factor_id

            new_factor_position = FactorPosition(entry_date=today,
                                                 product_id=product_id,
                                                 factor_id=factor_id,
                                                 notional_usd=notional_usd,
                                                 coeff=coeff,
                                                 parent_fund_id=parent_fund_id)

            factor_position_list.append(new_factor_position)

    if factor_position_list:
        session.add_all(factor_position_list)
        session.commit()


if __name__ == "__main__":
    download_factor_position()
