import './index.css'
import { Header } from "../../../components/Header";
import { useApp } from "../../../layout/AppContext";
import { CartItem } from '../../../components/CartItem';
import { Button, Col, Image, Row } from 'antd';
import { currency } from '../../../constantVars';

export const Cart = () => {
    const { cart, allProducts } = useApp()

    const getCartProducts = () => {
        const cartProducts = []
        for (let product of allProducts) {
            for (let item of cart) {
                if (product.uuid === item.productId) {
                    cartProducts.push({ ...product, quantity: item.quantity })
                }
            }
        }
        return cartProducts
    }

    const getZeroStateScreen = () => {
        return (
            <div className='cart-zero-state-container'>
                <h1 style={{ margin: '20px 0 40px 0' }}>Nothing's in here 📭</h1>
                <Image src='/images/emptyCart.svg' preview={false} width={450} />
            </div>
        )
    }

    const getSubTotal = () => {
        let subtotal = 0;
        for (let item of getCartProducts()) {
            subtotal = subtotal + item.price * item.quantity
        }
        return subtotal
    }

    const getCartItems = () => {
        return (<>
            {getCartProducts().map(({ uuid, title, price, quantity }, index) => <CartItem key={`${index}`} {...({ uuid, title, price, quantity })} />)}
            <div className='bottom-container'>
                <div></div>
                <div className='subtotal-container' >
                    <p className='subtotal-label' >subtotal</p>
                    <p className='subtotal' >{currency.rupee.symbol}&nbsp;{getSubTotal()}</p>
                </div>
            </div>
        </>
        )
    }

    return <>
        <Header style={{ marginBottom: "30px" }} title={'Cart 🛒'} >
            <Button type='primary' size='large'>Proceed to checkout</Button>
        </Header>
        {cart && cart.length === 0 ? getZeroStateScreen() : getCartItems()}
    </>;
};
