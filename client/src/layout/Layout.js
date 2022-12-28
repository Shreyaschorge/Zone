import React from 'react';
import { ExportOutlined, FullscreenExitOutlined, FullscreenOutlined } from '@ant-design/icons';
import { Button, Layout as AntLayout, Menu, } from 'antd';
import { useHistory } from 'react-router-dom'
import './layout.css'

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
    }
]

const Layout = ({ children }) => {
    const { push } = useHistory()

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
                    <Button
                        type="default"
                        size='large'
                        icon={<ExportOutlined />}
                    // onClick={() => enterLoading(1)}
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

