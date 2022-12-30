import './index.css'
import { useState, useEffect, useCallback } from 'react'
import { Header } from "../../../components/Header";
import { useApp } from '../../../layout/AppContext';
import Axios from '../../../utils/api'
import { OrderItem } from './OrderItem'
import { Col, Image, Row } from 'antd';

export const OrderList = () => {

    const { setErrors } = useApp()
    const [orders, setOrders] = useState([])

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
                {orders && orders.map((order, index) => <Col span={24} key={`${index}`}><OrderItem {...({ order, setOrders, orders })} /></Col>)}
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
