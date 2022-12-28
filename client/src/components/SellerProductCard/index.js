import { Card } from 'antd';
import { EditOutlined } from '@ant-design/icons'
import { currency } from '../../constantVars'

const { Meta } = Card;

export const ProductCard = ({ title, description, price }) => {
    return <Card
        style={{ width: 300 }}
        // cover={
        //     <img
        //         alt="example"
        //         src="https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png"
        //     />
        // }
        actions={[
            <EditOutlined key="edit" />,
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
}