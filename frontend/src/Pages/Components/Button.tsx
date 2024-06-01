import React, { Children } from 'react'

interface Props{
    children : string;
    type : string;
    disability : boolean;
    onButtonClicked : () => void;
}

const Button = ({children, type, onButtonClicked, disability} : Props) => {
  return (
    <button type="button" className={"btn btn-"+type} onClick={onButtonClicked} disabled={disability}>{children}</button>
  )
}

export default Button