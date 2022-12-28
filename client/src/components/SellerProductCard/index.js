import { useState } from 'react';
import { Card, Input, InputNumber, notification } from 'antd';
import { EditOutlined } from '@ant-design/icons'
import { currency } from '../../constantVars'
import { useApp } from '../../layout/AppContext'
import Axios from '../../utils/api'

import { Modal } from 'antd';

const { Meta } = Card;

export const ProductCard = ({ title: t, description: d, price: p, uuid, fetchUsersProducts }) => {

    const { setErrors } = useApp()

    const [title, setTitle] = useState(t);
    const [description, setDescription] = useState(d);
    const [price, setPrice] = useState(p);

    const [isModalOpen, setIsModalOpen] = useState(false);

    const showModal = () => {
        setIsModalOpen(true);
    };

    const handleOk = async () => {
        try {
            await Axios.put(`/products/${uuid}`, {
                title,
                description,
                price
            })

            notification.success({
                message: 'Product Updated Successfully',
                placement: 'bottomRight'
            })
            fetchUsersProducts()
            setIsModalOpen(false);
        } catch (err) {
            setErrors(err.response.data.errors)
        }
    };

    const handleCancel = () => {
        setIsModalOpen(false);
    };

    return <>
        <Card
            style={{ width: 300 }}
            actions={[
                <EditOutlined key="edit" onClick={() => showModal()} />,
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
        <Modal title="Edit Product" open={isModalOpen} onOk={handleOk} onCancel={handleCancel}>
            <div className='form-container'>
                <div className='form-fields'>
                    <label>Name</label>
                    <Input
                        size='large'
                        autoComplete='off'
                        placeholder='Royal Enfield Hunter 350'
                        value={title}
                        onChange={e => setTitle(e.target.value)}
                    />
                </div>
                <div className='form-fields'>
                    <label>Description</label>
                    <Input
                        size='large'
                        autoComplete='off'
                        placeholder='The Royal Enfield Hunter 350 is powered by a 349cc BS6 engine which develops a power of 20.2 BHP and a torque of 27 Nm.'
                        value={description}
                        onChange={e => setDescription(e.target.value)}
                    />
                </div>
                <div className='form-fields'>
                    <label>Price</label>
                    <div>
                        <InputNumber
                            size='large'
                            autoComplete='off'
                            placeholder='149000'
                            value={price}
                            prefix={currency.rupee.symbol}
                            onChange={value => setPrice(value)}
                            controls={false}
                            precision={2}
                            type='number'
                            style={{ width: '100%' }}
                        />
                    </div>

                </div>
            </div>

        </Modal>
    </>


}