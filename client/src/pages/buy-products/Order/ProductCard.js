import './ProductCard.css'
import { currency } from '../../../constantVars'


export const ProductCard = ({ title, price, quantity }) => {

    return <div className='cart-item-container' >
        <div className='title-container'>
            {title}
        </div>
        <div className='quantity-container'>
            {quantity}
        </div>
        <div className='price-container'> {currency.rupee.symbol}&nbsp;{price * quantity}</div>
    </div>


}