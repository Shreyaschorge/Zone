import './index.css'
import { Typography } from 'antd'

const { Text } = Typography

export const Header = ({ title, titleSuffix, children, ...rest }) => {
    return <div {...rest} className='container'>
        <div className='title-container'>
            <Text ellipsis={{
                tooltip: title,
            }} className={'title'}>{title}</Text>
            {titleSuffix()}
        </div>
        {children}
    </div>
}

Header.defaultProps = {
    titleSuffix: () => <></>
}