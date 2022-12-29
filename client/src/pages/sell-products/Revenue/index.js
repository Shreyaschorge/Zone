import './module.index.css'
import { useEffect, useCallback, useState } from 'react';
import { Header } from '../../../components/Header'
import { currency } from '../../../constantVars';
import { useApp } from '../../../layout/AppContext';
import Axios from '../../../utils/api';
import { Badge, Card, Col, Image, Row } from 'antd';
import Meta from 'antd/es/card/Meta';


const orderList = [
    {
        uuid: "order_1uqogqKtnVz4FC_nYfJxajt3YChkso",
        userId: "user_5WubOWgg48ZvsQqRgADF08fSML8BNM",
        status: "completed",
        products: [
            {
                title: "Buddha Idol",
                price: 500,
                description: "Have a calming presence, when you look at it.",
                uuid: "product_VjweRd_6UzMmj6zrMfzm-TtLlxIgHC",
                userId: "user_2Uwh4WCqq1VuawBlIIZZH_Ox1HC6Fv",
                quantity: 2
            },
            {
                title: "Plant Vase",
                price: 200,
                description: "White hexagonal vase for bamboo plant.",
                uuid: "product_wroaTo0oBXg9qzMDWPA4u1zXozgIwY",
                userId: "user_2Uwh4WCqq1VuawBlIIZZH_Ox1HC6Fv",
                quantity: 10
            }
        ]
    },
    {
        uuid: "order_EWJqcHzTXWx9moMcSywXs02fMqzJUD",
        userId: "user_5WubOWgg48ZvsQqRgADF08fSML8BNM",
        status: "completed",
        products: [
            {
                title: "Buddha Idol",
                price: 500,
                description: "Have a calming presence, when you look at it.",
                uuid: "product_VjweRd_6UzMmj6zrMfzm-TtLlxIgHC",
                userId: "user_2Uwh4WCqq1VuawBlIIZZH_Ox1HC6Fv",
                quantity: 3
            }
        ]
    },
    {
        uuid: "order_ly48pfEvRR1ZZD7TvZ8OG3V6tlrujD",
        userId: "user_5WubOWgg48ZvsQqRgADF08fSML8BNM",
        status: "completed",
        products: [
            {
                title: "Buddha Idol",
                price: 500,
                description: "Have a calming presence, when you look at it.",
                uuid: "product_VjweRd_6UzMmj6zrMfzm-TtLlxIgHC",
                userId: "user_2Uwh4WCqq1VuawBlIIZZH_Ox1HC6Fv",
                quantity: 2
            },
            {
                title: "Plant Vase",
                price: 200,
                description: "White hexagonal vase for bamboo plant.",
                uuid: "product_wroaTo0oBXg9qzMDWPA4u1zXozgIwY",
                userId: "user_2Uwh4WCqq1VuawBlIIZZH_Ox1HC6Fv",
                quantity: 8
            }
        ]
    }
]

export const Revenue = () => {
    const { setErrors } = useApp()

    const [soldProductsOrders, setSoldProductsOrders] = useState(orderList)

    const fetchSoldProducts = useCallback(async () => {
        try {
            const { data } = await Axios.get('/orders/soldProducts')
            setSoldProductsOrders(data);
        } catch (err) {
            setErrors(err.response.data.errors)
        }
    }, [])

    useEffect(() => {
        fetchSoldProducts()
    }, [])

    const getTotalRevenueAndProducts = useCallback(() => {
        let revenue = 0;
        let products = {}

        for (let order of soldProductsOrders) {
            for (let product of order.products) {
                revenue = revenue + (product.price * product.quantity)

                if (!products[product.uuid]) {
                    products[product.uuid] = product
                } else {
                    products[product.uuid] = { ...products[product.uuid], quantity: products[product.uuid].quantity + product.quantity }
                }
            }
        }
        return { revenue, products: Object.values(products) }
    }, [soldProductsOrders])

    const getZeroStateScreen = () => {
        return (
            <div className='zero-state-container'>
                <h1 style={{ margin: '20px 0 40px 0' }}> No one's buying 😞...</h1>
                <Image src='/images/zeroState4.svg' preview={false} width={450} />
            </div>
        )
    }


    const getRevenueScreen = () => {
        return (
            <Row gutter={[16, 16]}>
                {getTotalRevenueAndProducts().products.map(({ title, description, price, quantity }, index) => {
                    return <Col key={`${index}`} span={6}>
                        <Badge.Ribbon color={"green"} text={`${currency.rupee.symbol} ${price * quantity}`}>
                            <Card
                                style={{ width: 300 }}
                            >
                                <Meta
                                    title={title}
                                    description={description}
                                />

                                <p style={{ fontSize: '20px', fontWeight: 300, margin: '20px 0 0 0', padding: 0 }}>
                                    Quantity &nbsp;{quantity}
                                </p>

                            </Card>
                        </Badge.Ribbon>

                    </Col>
                })}
            </Row>
        )
    }

    return <>
        <Header title='🤫 Revenue'>
            <div className='revenue-val-container'>
                <p className='revenue-value' >{currency.rupee.symbol}&nbsp;{getTotalRevenueAndProducts().revenue}</p>
            </div>
        </Header>
        {
            soldProductsOrders && soldProductsOrders.length === 0 ? getZeroStateScreen() : getRevenueScreen()
        }
    </>;
};
