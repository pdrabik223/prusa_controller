
import type { IconType } from "react-icons";
import { Row } from "./row"
import { RiSettingsLine } from "react-icons/ri";
import { Column } from "./Column";
import { useState } from "react";

function App() {

  return <>
    <Header />
    <h1> Main Status Page</h1>

    <button> Connect To printer</button>

    <p> gcode file upload for printing </p>


    <p>Svg to gcode</p>
    <p>Svg to gcode</p>



  </>

}

export default App



export const MainPage: React.FC<{}> = () => {

  return <></>

}


export const Header: React.FC<{}> = () => {

  return <div style={{
    // width: "100%",
    // height: "60px",
    // position: 'sticky',
    // top: '0px',
    // left: '0px',
    // backgroundColor: "red",
    // margin: 'auto',
    // padding: '10px 16px'

    position: "sticky",
    height: "80px",
    width: "96%",
    left: "2%",
    right: "2%",
    top: "0px",
    display: 'flex',
    backgroundColor: 'transparent',
    alignItems: 'center',
    margin: 'auto',
  }}>
    <TextButton text={<h2 style={{ fontSize: 'xx-large' }}>Prusa MK3s</h2>} onPress={() => { }} />
    <Row>{null}</Row>
    <IconButton style={{ right: "0" }} icon={<RiSettingsLine size="60px" />} onPress={() => { }} />
  </div>

}

interface IconButtonProps {
  icon: React.ReactNode
  onPress: () => void
  style?: React.CSSProperties

}

export const IconButton: React.FC<IconButtonProps> = (props: IconButtonProps) => {
  const [isHovering, setIsHovering] = useState(false)

  return <div
    onMouseEnter={() => setIsHovering(true)}
    onMouseLeave={() => setIsHovering(false)}

    onClick={props.onPress}
    className="icon_button"
    style={
      (() => {
        const baseStyle: React.CSSProperties = {
          position: 'relative',
          color: isHovering ? 'orange' : undefined,
          cursor: isHovering ? 'pointer' : undefined
        };

        return { ...baseStyle, ...(props.style || {}) } as React.CSSProperties;
      })()}
  > {props.icon}</div >

}


interface TextButtonProps {
  text: React.ReactNode
  onPress: () => void
  style?: React.CSSProperties

}

export const TextButton: React.FC<TextButtonProps> = (props: TextButtonProps) => {
  const [isHovering, setIsHovering] = useState(false)

  return <div
    onMouseEnter={() => setIsHovering(true)}
    onMouseLeave={() => setIsHovering(false)}
    onClick={props.onPress}
    className="icon_button"
    style={
      (() => {
        const baseStyle: React.CSSProperties = {
          position: 'relative',
          color: isHovering ? 'orange' : undefined,
          cursor: isHovering ? 'pointer' : undefined
        };

        return { ...baseStyle, ...(props.style || {}) } as React.CSSProperties;
      })()}
  > {props.text}</div >

}

