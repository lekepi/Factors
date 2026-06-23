from models import session, FactorMarketData, FactorPosition, Position, Product
from datetime import date


def download_factor_position(my_date):
    session.query(FactorPosition).filter(FactorPosition.entry_date == my_date).delete()
    session.commit()

    factor_md_list = session.query(FactorMarketData).filter(FactorMarketData.entry_date == my_date).all()
    position_list = session.query(Position).filter(Position.entry_date == my_date).all()

    factor_position_list = []

    for position in position_list:

        product_id = position.product_id
        notional_usd = position.mkt_value_usd
        parent_fund_id = position.parent_fund_id

        factor_md_matches = [f for f in factor_md_list if f.ticker == position.product.ticker]
        for factor_md in factor_md_matches:
            raw_value = factor_md.raw_value
            linear_value = factor_md.linear_value
            norm_value = factor_md.norm_value
            quintile = factor_md.quintile
            index = factor_md.index

            factor_id = factor_md.factor_id

            new_factor_position = FactorPosition(entry_date=my_date,
                                                 product_id=product_id,
                                                 factor_id=factor_id,
                                                 notional_usd=notional_usd,
                                                 parent_fund_id=parent_fund_id,
                                                 raw_value=raw_value,
                                                 linear_value=linear_value,
                                                 norm_value=norm_value,
                                                 quintile=quintile,
                                                 index=index)

            factor_position_list.append(new_factor_position)

    if factor_position_list:
        session.add_all(factor_position_list)
        session.commit()


if __name__ == "__main__":
    my_date1 = date(2022, 6, 24)
    my_date2 = date(2022, 7, 15)
    download_factor_position(my_date1)
    download_factor_position(my_date2)
