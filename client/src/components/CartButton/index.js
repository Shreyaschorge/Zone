import './index.css'
import { ShoppingCartOutlined } from "@ant-design/icons"
import { Badge, Button } from "antd"
import { useHistory } from "react-router-dom"

export const CartButton = () => {

    // #FF4D4E 

    const { push } = useHistory()

    return <div style={{ marginRight: '10px', position: "relative" }}>
        <span className="avatar-item">
            <Badge count={1}>
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