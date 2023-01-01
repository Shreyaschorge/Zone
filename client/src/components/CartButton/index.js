import './index.css'
import { ShoppingCartOutlined } from "@ant-design/icons"
import { Badge, Button } from "antd"
import { useHistory } from "react-router-dom"
import { useApp } from '../../layout/AppContext'

export const CartButton = () => {

    const { cart } = useApp()

    const { push } = useHistory()

    const getProductsCount = () => {
        let count = 0;
        for (let item of cart) {
            count = count + item.quantity
        }
        return count
    }

    return <div style={{ marginRight: '10px', position: "relative" }}>
        <span className="avatar-item">
            <Badge count={getProductsCount()}>
                <Button
                    type="default"
                    size='large'
                    icon={<ShoppingCartOutlined />}
                    onClick={() => push('/buy-products/cart')}
                />
            </Badge>
        </span>
    </div>

}