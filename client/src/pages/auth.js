import './auth.css'

import { useState } from 'react';
import { Col, Row, Input, Button, Image, notification } from 'antd';
import { UserOutlined, KeyOutlined } from '@ant-design/icons';
import { useHistory } from 'react-router-dom'
import Axios from '../utils/api'
import Token from '../utils/manageToken';

export const Auth = () => {

    const { push } = useHistory()

    const [showResigterScreen, setShowRegisterScreen] = useState(false)
    const [regEmail, setRegEmail] = useState('')
    const [regPass, setRegPass] = useState('')
    const [regRePass, setRegRePass] = useState('')
    const [loginEmail, setLoginEmail] = useState('')
    const [loginPass, setLoginPass] = useState('')


    const handleRegister = async () => {
        if (regEmail === "" || regPass === "" || regRePass === "") {
            notification.error({
                message: "Please enter the details",
                placement: 'bottomRight'
            })
        } else if (regPass !== regRePass) {
            notification.error({
                message: "Password does not match",
                placement: 'bottomRight'
            })
        } else {
            try {
                await Axios.post('/users/register', { 'email': regEmail, 'password': regPass })
                notification.success({
                    message: "Account created successfully",
                    placement: 'bottomRight'
                })
                setShowRegisterScreen(showResigterScreen => !showResigterScreen)

            } catch (err) {
                // handle error
            }
        }
    }

    const handleLogin = async () => {
        if (loginEmail === "" || loginPass === "") {
            notification.error({
                message: "Please enter the details",
                placement: 'bottomRight'
            })
        } else {
            try {
                const { data } = await Axios.post('/users/login', { 'email': loginEmail, 'password': loginPass })
                notification.success({
                    message: "Logged in successfully",
                    placement: 'bottomRight'
                })
                if (data.access_token) {
                    Token.setUser(data)
                }
                push("/")
                window.location.reload()
            } catch (err) {
                // handle error
            }
        }
    }

    const registerScreen = () => {
        return (
            <Row>
                <Col span={12}>
                    <div className='left-container'>
                        <Image src='/images/register.svg' width={500} preview={false} />
                    </div>
                </Col>
                <Col span={12}>
                    <div className='right-container'>
                        <h1 className='header'>Welcome to Zone 👽</h1>
                        <div className='description'>
                            <p>Zone is an on-demand C2C where you can buy as well as sell products.</p>
                        </div>

                        <div className='form-fields'>
                            <label>Email</label>
                            <Input
                                size='large'
                                autoComplete='off'
                                placeholder='john@doe.com'
                                prefix={<UserOutlined style={{ marginRight: '10px' }} />}
                                value={regEmail}
                                onChange={e => setRegEmail(e.target.value)}
                            />
                        </div>
                        <div className='form-fields'>
                            <label>Password</label>
                            <Input.Password
                                size='large'
                                autoComplete='off'
                                placeholder='*************'
                                prefix={<KeyOutlined style={{ marginRight: '10px' }} />}
                                value={regPass}
                                onChange={e => setRegPass(e.target.value)}
                            />
                        </div>
                        <div className='form-fields'>
                            <label>Re-enter Password</label>
                            <Input.Password
                                size='large'
                                placeholder='*************'
                                prefix={<KeyOutlined style={{ marginRight: '10px' }} />}
                                value={regRePass}
                                onChange={e => setRegRePass(e.target.value)}
                            />
                        </div>

                        <div className='form-fields'>
                            {
                                <Button size='large' type="primary" style={{ width: '100%' }} onClick={handleRegister}>Register</Button>
                            }

                        </div>

                        <p className='have-account' onClick={() => { setShowRegisterScreen(showResigterScreen => !showResigterScreen) }} >Already have an account...?</p>
                    </div>

                </Col>
            </Row>
        )
    }

    const loginScreen = () => {
        return (
            <Row>
                <Col span={12}>
                    <div className='left-container'>
                        <Image src='/images/login.svg' width={500} preview={false} />
                    </div>
                </Col>
                <Col span={12}>
                    <div className='right-container'>
                        <h1 className='header'>Login 🗝</h1>

                        <div className='form-fields'>
                            <label>Email</label>
                            <Input
                                size='large'
                                autoComplete='off'
                                placeholder='john@doe.com'
                                prefix={<UserOutlined style={{ marginRight: '10px' }} />}
                                value={loginEmail}
                                onChange={e => setLoginEmail(e.target.value)}
                            />
                        </div>
                        <div className='form-fields'>
                            <label>Password</label>
                            <Input.Password
                                size='large'
                                autoComplete='off'
                                placeholder='*************'
                                prefix={<KeyOutlined style={{ marginRight: '10px' }} />}
                                value={loginPass}
                                onChange={e => setLoginPass(e.target.value)}
                            />
                        </div>

                        <div className='form-fields'>

                            <Button size='large' type="primary" style={{ width: '100%' }} onClick={handleLogin}>Login</Button>
                        </div>

                        <p className='have-account' onClick={() => { setShowRegisterScreen(showResigterScreen => !showResigterScreen) }}>Don't have an account...?</p>
                    </div>

                </Col>
            </Row>
        )
    }

    return (
        showResigterScreen ? registerScreen() : loginScreen()
    )
}