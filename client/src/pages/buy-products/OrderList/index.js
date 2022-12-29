import './index.css'
import { useState, useEffect, useCallback } from 'react'
import { Header } from "../../../components/Header";
import { useApp } from '../../../layout/AppContext';
import Axios from '../../../utils/api'
import { OrderItem } from './OrderItem'
import { Col, Image, Row } from 'antd';

const orderList = [
    {
        uuid: "order_1uqogqKtnVz4FC_nYfJxajt3YChkso",
        userId: "user_5WubOWgg48ZvsQqRgADF08fSML8BNM",
        status: "draft",
        products: [
            {
                title: "Buddha Idol",
                price: 500,
                description: "Have a calming presence, when you look at it.",
                uuid: "product_VjweRd_6UzMmj6zrMfzm-TtLlxIgHC",
                userId: "user_2Uwh4WCqq1VuawBlIIZZH_Ox1HC6Fv",
                quantity: 5
            },
            {
                title: "Plant Vase",
                price: 200,
                description: "White hexagonal vase for bamboo plant.",
                uuid: "product_wroaTo0oBXg9qzMDWPA4u1zXozgIwY",
                userId: "user_2Uwh4WCqq1VuawBlIIZZH_Ox1HC6Fv",
                quantity: 2
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
        status: "cancelled",
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

export const OrderList = () => {

    const { setErrors } = useApp()
    const [orders, setOrders] = useState(orderList)

    const fetchAllOrders = useCallback(async () => {
        try {
            const { data } = await Axios.get('/orders');
            setOrders(data)
        } catch (err) {
            setErrors(err.response.data.errors)
        }
    }, [])

    useEffect(() => {
        fetchAllOrders()
    }, [])

    const getOrders = () => {
        return <div style={{ margin: "30px 60px 0px 60px" }}>
            <Row gutter={[0, 16]}>
                {orders.map((order, index) => <Col span={24} key={`${index}`}><OrderItem order={order} /></Col>)}
            </Row>
        </div>

    }

    const getZeroStateScreen = () => {
        return (
            <div className='zero-state-container'>
                <h1 style={{ margin: '20px 0 40px 0' }}>Nothing's in here 📭</h1>
                <Image src='/images/zeroState3.svg' preview={false} width={450} />
            </div>
        )
    }

    return <>
        <Header title={'🗒 Your Orders'} />
        {orders && orders.length === 0 ? getZeroStateScreen() : getOrders()}
    </>;
};
