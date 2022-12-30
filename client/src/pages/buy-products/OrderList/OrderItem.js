import { Badge, Button, Collapse, notification } from "antd"
import { ProductCard } from '../Order/ProductCard'
import { useHistory } from 'react-router-dom'
import Axios from "../../../utils/api"
import { useApp } from '../../../layout/AppContext'

const { Panel } = Collapse;

const BadgeColor = {
    draft: "blue",
    completed: "green",
    cancelled: "red"
}

export const OrderItem = ({ order, orders, setOrders }) => {

    const { push } = useHistory()
    const { setErrors } = useApp()

    const getBadgeColor = () => {
        return BadgeColor[order.status]
    }

    const handleCancel = async () => {
        try {
            const { data } = await Axios.put(`/orders/cancelOrder/${order.uuid}`)
            notification.success({
                message: data.message,
                placement: "bottomRight"
            })
            setOrders(orders.map(o => o.uuid === order.uuid ? { ...o, status: 'cancelled' } : o))
        } catch (err) {
            setErrors(err.response.data.errors)
        }
    }

    return <>
        <Badge.Ribbon text={order.status} color={getBadgeColor()}>
            <Collapse bordered={true}>
                <Panel showArrow={true} header={order.uuid} >
                    <div style={styles.ButtonContainer}>
                        {order.status === 'draft' && <div>
                            <Button style={{ marginRight: '10px' }} onClick={() => push(`/buy-products/orders/${order.uuid}`)} >View Order</Button>
                            <Button danger onClick={handleCancel} >Cancel Order</Button>
                        </div>}
                    </div>
                    {order && order.products && order.products.map(({ title, price, quantity }, index) => <ProductCard key={`${index}`} {...({ title, price, quantity })} />)}
                </Panel>
            </Collapse>
        </Badge.Ribbon>
    </>
}

const styles = {
    ButtonContainer: {
        width: "100%",
        display: 'flex',
        justifyContent: 'flex-end'
    }
}