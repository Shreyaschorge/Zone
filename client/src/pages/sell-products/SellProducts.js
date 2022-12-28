import './SellProducts.css'
import { useState } from 'react';
import { Button, Modal, notification, Input, InputNumber, Row, Col } from 'antd'
import { ProductCard } from '../../components/SellerProductCard'

import { Header } from '../../components/Header'
import { currency } from '../../constantVars'
import Axios from '../../utils/api'
import { useApp } from '../../layout/AppContext'

const products = [
  {
    title: 'Test this',
    description: 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean m',
    price: 344.56
  },
  {
    title: 'Test this',
    description: 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean m',
    price: 344.56
  },
  {
    title: 'Test this',
    description: 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean m',
    price: 344.56
  },
  {
    title: 'Test this',
    description: 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean m',
    price: 344.56
  },
  {
    title: 'Test this',
    description: 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean m',
    price: 344.56
  },
  {
    title: 'Test this',
    description: 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean m',
    price: 344.56
  },
  {
    title: 'Test this',
    description: 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean m',
    price: 344.56
  },
]

export const SellProducts = () => {

  const { setErrors } = useApp()

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [price, setPrice] = useState('')

  const clearFields = () => {
    setPrice('')
    setDescription('')
    setTitle('')
  }

  const showModal = () => {
    setIsModalOpen(true);
  };

  const handleOk = async () => {
    try {

      // await Axios.post('/products', {
      //   title,
      //   description,
      //   price
      // })

      products.push({
        title,
        description,
        price
      })

      notification.success({
        message: 'Product Added Successfully',
        placement: 'bottomRight'
      })
      setIsModalOpen(false);
      clearFields()
    } catch (err) {
      setErrors(err.response.data.errors)
    }

  };
  const handleCancel = () => {
    setIsModalOpen(false);
  };

  return <>
    <Header style={{ marginBottom: "30px" }} title={'Your Products'}>
      <Button type='primary' size='large' onClick={showModal} >Add Product</Button>
    </Header>

    <Row gutter={[16, 16]} >
      {products.map(({ title, description, price }) => <Col className="gutter-row" span={6}><ProductCard {...({ title, description, price })} /></Col>)}
    </Row>



    <Modal title="Basic Modal" open={isModalOpen} onOk={handleOk} onCancel={handleCancel}>
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
  </>;
};
