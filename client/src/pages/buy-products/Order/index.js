import { useCallback, useEffect, useState } from 'react'
import jwt_decode from "jwt-decode";
import { useParams, useHistory } from 'react-router-dom';
import { useApp } from '../../../layout/AppContext';
import Axios from '../../../utils/api'
import { Header } from '../../../components/Header'
import { notification, Tag } from 'antd';
import { ProductCard } from './ProductCard'
import { currency } from '../../../constantVars';
import StripeCheckout from 'react-stripe-checkout';
import Token from '../../../utils/manageToken';


const _order = {
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
            quantity: 1

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
}

const TagColor = {
    draft: "blue",
    completed: "success",
    cancelled: "error"
}

export const Order = () => {
    const { orderId } = useParams();
    const { push } = useHistory()
    const { setErrors } = useApp()

    const [order, setOrder] = useState(_order)

    const fetchOrder = useCallback(async () => {
        if (orderId) {
            try {
                const { data } = await Axios.get(`/orders/${orderId}`)
                setOrder(data)
            } catch (err) {
                setErrors(err.response.data.errors)
            }
        }

    }, [])

    useEffect(() => {
        if (orderId) {
            fetchOrder()
        }
    }, [orderId])

    const getSubTotal = () => {
        let subtotal = 0
        for (let prod of order.products) {
            subtotal = subtotal + (prod.price * prod.quantity)
        }
        return subtotal
    }

    const handleCheckout = async (token) => {
        try {
            await Axios.post('/payments', {
                orderId,
                token
            })
            notification.success({
                message: 'Payment created successfully',
                placement: 'bottomRight'
            })
            push('/sell-products/paidProducts')
        } catch (err) {
            setErrors(err.response.data.errors)
        }
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



    const getProducts = () => {
        return (
            <>
                {order.products.map(({ price, title, quantity }, index) => <ProductCard key={`${index}`} {...({ price, title, quantity })} />)}

                <div className='bottom-container'>
                    <div >
                    </div>
                    <div className='subtotal-container' >
                        <p className='subtotal-label' >subtotal</p>
                        <p className='subtotal' >{currency.rupee.symbol}&nbsp;{getSubTotal()}</p>
                    </div>
                </div>
            </>
        )
    }

    return (<>
        {
            order
                ?
                <>
                    <Header style={{ marginBottom: "30px" }} title={`📝 ${orderId} `} titleSuffix={getOrderStatus}>
                        {order.status === 'draft'
                            && <StripeCheckout
                                token={({ id }) => handleCheckout(id)}
                                stripeKey={process.env.STRIPE_PK}
                                amount={parseInt(getSubTotal() * 100)}
                                currency='inr'
                                email={jwt_decode(Token.getLocalAccessToken()).sub.email}
                            />}
                    </Header>
                    {getProducts()}
                </>
                : <></>
        }
    </>)
};
