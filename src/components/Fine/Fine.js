import React from "react";
import { Input } from "semantic-ui-react";
import { Button } from "semantic-ui-react";
import { Table } from "semantic-ui-react";
import { Divider, Segment, Header, Icon, Label } from "semantic-ui-react";

export default class Fine extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      rcFound: false,
      rcnum: "-",
      name: "-",
      phone: "-",
      address: "-",
      make: "-",
      model: "-",
      fineSent: false
    };
  }
  showDetails = () => {
    this.setState({
      rcFound: true,
      rcnum: "KA04G860",
      name: "Rakesh Ohja",
      phone: "+91 90241 43281",
      address: "#64, Twin Towers, Bangalore",
      make: "Hyundai Ltd.",
      model: "Verna Sportz"
    });
  };

  sendFine = () => {
    this.setState({
      fineSent: true
    });
  };

  render() {
    return (
      <div style={styles.center}>
        <div style={styles.form} className="fine">
          <Header as="h3">
            <Icon name="search" />
            <Header.Content>
              Find License Plate
              <Header.Subheader>Find the owner of the vehicle</Header.Subheader>
            </Header.Content>
          </Header>
          <Input placeholder="Enter Plate Number - KA04G860" value="KA04G860" />
          <br />
          <Button primary onClick={() => this.showDetails()}>
            FIND VEHICLE
          </Button>
          <br />
          <br />
          <Divider section />
          
          {this.state.rcFound && (<div className="challan"><Header as="h3">
            <Icon name="money" />
            <Header.Content>
              Send Fine
              <Header.Subheader>Send fine to owner's phone</Header.Subheader>
            </Header.Content>
          </Header>

          <Input labelPosition="right" type="text" placeholder="Fine Amount">
            <Label basic>&#8377;</Label>
            <input />
            <Label>.00</Label>
          </Input>
          <br />
          {this.state.fineSent && <Button color="green"><Icon name="check" /> FINE SENT</Button> }
          {!this.state.fineSent && <Button color="blue" onClick={() => this.sendFine()}>SEND FINE</Button> }
          </div>)
          }

        </div>
        <div className="rc-info">
          {!this.state.rcFound && (
            <img
              className="car-placeholder"
              src="https://image.freepik.com/free-icon/car-black-side-silhouette_318-43519.jpg"
            />
          )}
          {this.state.rcFound && (
            <img src="https://www.motorbeam.com/wp-content/uploads/Hyundai-Verna-Brown.jpg" />
          )}
          <Table singleLine>
            <Table.Header>
              <Table.Row>
                <Table.HeaderCell colSpan="2">
                  REGISTRATION CERTIFICATE INFO
                </Table.HeaderCell>
              </Table.Row>
            </Table.Header>

            <Table.Body>
              <Table.Row>
                <Table.Cell>Registration Number</Table.Cell>
                <Table.Cell>{this.state.rcnum}</Table.Cell>
              </Table.Row>
              <Table.Row>
                <Table.Cell>Owner's Name</Table.Cell>
                <Table.Cell>{this.state.name}</Table.Cell>
              </Table.Row>
              <Table.Row>
                <Table.Cell>Owner's Phone</Table.Cell>
                <Table.Cell>{this.state.phone}</Table.Cell>
              </Table.Row>
              <Table.Row>
                <Table.Cell>Address</Table.Cell>
                <Table.Cell>{this.state.address}</Table.Cell>
              </Table.Row>
              <Table.Row>
                <Table.Cell>Make</Table.Cell>
                <Table.Cell>{this.state.make}</Table.Cell>
              </Table.Row>
              <Table.Row>
                <Table.Cell>Model</Table.Cell>
                <Table.Cell>{this.state.model}</Table.Cell>
              </Table.Row>
            </Table.Body>
          </Table>
        </div>
      </div>
    );
  }
}

const styles = {
  center: {
    display: "flex",
    justifyContent: "center",
    height: "100%",
    padding: 20
  },
  form: {
    display: "flex",
    flexDirection: "column",
    padding: 20
  }
};
