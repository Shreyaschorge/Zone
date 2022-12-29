import { useCallback, useEffect, useState } from 'react'
import { useParams } from 'react-router-dom';
import { useApp } from '../../../layout/AppContext';
import Axios from '../../../utils/api'
import { Header } from '../../../components/Header'
import { Button, Tag } from 'antd';

const _order = {
    uuid: "order_wergupwerhierfwerwgerjhb",
    userId: "user_buyer",
    status: "draft",
    products: [
        {
            title: "Royal Enfield Hunter 350",
            price: 890,
            description: "The Royal Enfield Hunter 350 is powered by a 349cc BS6 engine",
            uuid: "product_1",
            userId: "user_seller"
        },
        {
            uuid: 'product_4',
            title: 'Kawasaki Ninja',
            description: 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean m',
            price: 10,
            userId: "user_seller"
        },
        {
            uuid: 'product_3',
            title: 'TVS Ronin',
            description: 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean m',
            price: 10,
            userId: "user_seller"
        },
    ]
}

const TagColor = {
    draft: "default",
    completed: "success",
    cancelled: "error"
}

export const Order = () => {
    const { orderId } = useParams();
    const { setErrors } = useApp()

    const [order, setOrder] = useState(_order)

    const fetchOrder = useCallback(async () => {
        try {
            const { data } = await Axios.get(`/orders/${orderId}`)
            setOrder(data)
        } catch (err) {
            setErrors(err.response.data.errors)
        }
    }, [])

    useEffect(() => {
        if (orderId) {
            fetchOrder()
        }
    }, [orderId])

    const handleCheckout = () => {

    }

    const getOrderStatus = () => {
        return <Tag style={{
            height: '30px',
            borderRadius: '50px',
            display: 'flex',
            alignItems: 'center',
        }} color={TagColor[order.status]}>
            {order.status}
        </Tag>
    }

    return (<>
        {
            order
                ?
                <Header style={{ marginBottom: "30px" }} title={`📝 ${orderId} `} titleSuffix={getOrderStatus}>
                    {order.status === 'draft' && <Button type='primary' size='large' onClick={handleCheckout}>Checkout</Button>}
                </Header>
                : <></>
        }
    </>)
};
