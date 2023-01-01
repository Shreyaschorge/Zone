import './module.index.css'
import { useEffect, useCallback, useState } from 'react';
import { Header } from '../../../components/Header'
import { currency } from '../../../constantVars';
import { useApp } from '../../../layout/AppContext';
import Axios from '../../../utils/api';
import { Badge, Card, Col, Image, Row } from 'antd';
import Meta from 'antd/es/card/Meta';

export const Revenue = () => {
    const { setErrors } = useApp()

    const [soldProductsOrders, setSoldProductsOrders] = useState([])

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
                                    {quantity}&nbsp;Sold
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
