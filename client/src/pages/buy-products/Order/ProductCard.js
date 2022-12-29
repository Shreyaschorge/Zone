import { Card } from 'antd';
import { ShoppingCartOutlined } from '@ant-design/icons'
import { currency } from '../../../constantVars'

const { Meta } = Card;

export const ProductCard = ({ title, description, price }) => {

    return <>
        <Card
            style={{ width: 300 }}
        // actions={[
        //     <ShoppingCartOutlined key="cart" onClick={addProductToCart} />,
        // ]}
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