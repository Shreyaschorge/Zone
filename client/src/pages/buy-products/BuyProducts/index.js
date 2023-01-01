import './index.css'
import { Col, Image, Row } from "antd";
import { useEffect, useCallback } from "react";
import { Header } from "../../../components/Header";
import { useApp } from '../../../layout/AppContext'
import Axios from "../../../utils/api";
import { ProductCard } from '../../../components/BuyerProductCard'

export const BuyProducts = () => {

  const { setErrors, allProducts, setAllProducts } = useApp()

  const fetchProducts = useCallback(async () => {
    try {
      const { data } = await Axios.get('/products');
      setAllProducts(data)
    } catch (err) {
      setErrors(err.response.dataa.errors)
    }
  }, [setErrors])

  useEffect(() => {
    fetchProducts()
  }, [])

  const getZeroStateScreen = () => {
    return (
      <div className='products-zero-state-container'>
        <h1 style={{ margin: '20px 0 40px 0' }}>Looks like no one wanna sell 🥲</h1>
        <Image src='/images/zeroState2.svg' preview={false} width={450} />
      </div>
    )
  }

  const getAllProductsScreen = useCallback(() => {
    return <Row gutter={[16, 16]} >
      {allProducts.map(({ title, description, price, uuid }, index) => <Col key={`${index}`} span={6}><ProductCard {...({ title, description, price, uuid })} /></Col>)}
    </Row>
  }, [allProducts])

  return <>
    <Header style={{ marginBottom: "30px" }} title={'🎊 Happy new year..'} />
    {allProducts && allProducts.length === 0 ? getZeroStateScreen() : getAllProductsScreen()}
  </>;
};
