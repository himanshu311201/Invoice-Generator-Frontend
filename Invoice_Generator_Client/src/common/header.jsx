import './css/header.css'
import { Header } from 'semantic-ui-react'
function commonHeader() {
  return (
      <Header as='h1' image='./public/logo192.png' content='Learn More' />
  );
}
export default commonHeader;