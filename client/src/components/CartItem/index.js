import './index.css'
import { CloseOutlined } from '@ant-design/icons';
import { InputNumber } from 'antd'
import { useState } from 'react'
import { useApp } from '../../layout/AppContext'
import { currency } from '../../constantVars';

export const CartItem = ({ uuid, title, price, quantity: q }) => {

    const { cart, setCart } = useApp()

    const [quantity, setQuantity] = useState(q)

    const handleQuantityChange = (val) => {
        setCart(cart.map(item => item.productId === uuid ? { productId: uuid, quantity: val } : item))
        setQuantity(val)
    }

    const handleRemoveItem = () => {
        setCart(cart.filter(item => item.productId !== uuid))
    }

    return <div className='cart-item-container' >
        <div className='title-container'>
            {title}
        </div>
        <div className='rest-container'>
            <InputNumber type={'number'} onChange={handleQuantityChange} min={1} value={quantity} />
        </div>
        <div className='price-container'> {currency.rupee.symbol}&nbsp;{price * quantity}</div>
        <div className='cancel-container'>
            <CloseOutlined onClick={handleRemoveItem} />
        </div>
    </div>
}