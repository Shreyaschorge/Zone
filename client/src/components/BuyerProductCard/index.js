import { Card, notification } from 'antd';
import { ShoppingCartOutlined } from '@ant-design/icons'
import { currency } from '../../constantVars'
import { useApp } from '../../layout/AppContext'

const { Meta } = Card;

export const ProductCard = ({ title, description, price, uuid }) => {

    const { cart, setCart } = useApp()

    const addProductToCart = () => {
        const existing_item = cart.find(({ productId }) => productId === uuid)

        if (!existing_item) {
            console.log("==> inside if")
            setCart([...cart, { productId: uuid, quantity: 1 }])
        } else {
            console.log("==> inside else")
            setCart(cart.map(item => item.productId === existing_item.productId
                ? { productId: existing_item.productId, quantity: existing_item.quantity + 1 }
                : item))
        }

    }

    return <>
        <Card
            style={{ width: 300 }}
            actions={[
                <ShoppingCartOutlined key="cart" onClick={addProductToCart} />,
            ]}
        >
            <Meta
                title={title}
                description={description}
            />

            <p style={{ fontSize: '20px', fontWeight: 300, margin: '20px 0 0 0', padding: 0 }}>
                {currency.rupee.symbol}&nbsp;{price}
            </p>

        </Card>
    </>


}