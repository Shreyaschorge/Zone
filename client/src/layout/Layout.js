import React from 'react';
import { BarChartOutlined, ExportOutlined, FullscreenExitOutlined, FullscreenOutlined, ShoppingCartOutlined } from '@ant-design/icons';
import { Button, Layout as AntLayout, Menu, notification, } from 'antd';
import { useHistory } from 'react-router-dom'
import './layout.css'
import Token from '../utils/manageToken'
import Axios from '../utils/api'
import { useApp } from './AppContext'
import { CartButton } from '../components/CartButton';

const { Header, Content, Sider } = AntLayout;

const menu = [
    {
        title: 'Buy Products',
        icon: <FullscreenExitOutlined />,
        path: '/buy-products',
    },
    {
        title: 'Sell Products',
        icon: <FullscreenOutlined />,
        path: '/sell-products',
    },
    {
        title: 'Paid Products',
        icon: <BarChartOutlined />,
        path: '/sell-products/paidProducts',
    }
]

const Layout = ({ children }) => {
    const { push } = useHistory()
    const { setErrors } = useApp()

    const handleLogout = async () => {
        try {
            await Axios.post('/users/logout')
            Token.removeUser()
            notification.success({
                message: "Logged out successfully",
                placement: 'bottomLeft'
            })
            push('/')
            window.location.reload()
        } catch (err) {
            setErrors(err.response.data.errors)
        }

    }

    return (
        <AntLayout style={{ height: "100vh" }}>
            <Sider
                breakpoint="lg"
                collapsedWidth="0"
            >
                <div className='logo-container'>
                    <p className='logo'>Zone 👽</p>
                </div>
                <Menu
                    theme="dark"
                    mode="inline"
                    defaultSelectedKeys={['4']}
                >
                    {menu.map(({ title, icon, path }, index) => {
                        return <Menu.Item icon={icon} key={String(`${index}`)} onClick={() => push(path)}>
                            {title}
                        </Menu.Item>
                    })}
                </Menu>
            </Sider>
            <AntLayout>
                <Header style={styles.header}>
                    <CartButton />
                    <Button
                        type="default"
                        size='large'
                        icon={<ExportOutlined />}
                        onClick={handleLogout}
                    >
                        Logout
                    </Button>
                </Header>
                <Content style={{ margin: '24px 16px 0' }}>
                    {children}
                </Content>
            </AntLayout>
        </AntLayout>
    );
};

const styles = {
    header: {
        background: "#fff",
        padding: '0 30px 0 0',
        display: 'flex',
        justifyContent: 'flex-end',
        alignItems: 'center',
        boxShadow: '0px 3px 9px gainsboro',
    }
}

export default Layout;

