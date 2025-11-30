import { Row } from "./row"
import { RiSettingsLine } from "react-icons/ri";
import { useState } from "react";
import { Canvas, useFrame, type Vector3 } from "@react-three/fiber";
import { useRef } from 'react'
import type { Mesh } from "three";


interface CubeProps {

  position: Vector3
  size: [number, number, number]

}

const Cube = (props: CubeProps) => {

  const ref = useRef<Mesh>(null)

  useFrame((state, delta) => {
    ref.current!.rotation.x += delta * 0.5
    ref.current!.rotation.y += delta * 0.75
  })

  return (
    <mesh
      position={props.position}
      ref={ref}
    >
      <boxGeometry args={props.size} />
      <meshStandardMaterial
        color={'orange'}
      />
    </mesh>
  )
}


function App() {

  return <>
    <Header />

    <button> Connect To printer</button>

    <p> gcode file upload for printing </p>
    <Canvas>

      <directionalLight position={[0, 0, 2]} />
      <ambientLight intensity={0.4} />

      <Cube position={[0, 0, 0]} size={[1, 5, 1]} />


    </Canvas>
    <p>Svg to gcode</p>
  </>

}

export default App



export const MainPage: React.FC<{}> = () => {

  return <></>

}


export const Header: React.FC<{}> = () => {

  return <div style={{

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

