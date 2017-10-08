import React, { Component } from 'react';
import logo from '../../images/raven.svg';

export default class Logo extends Component {
  render() {
    return (
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          padding: 20
        }}
      >
        <img src={logo} alt="" style={{ width: '80px', height: '80px' }} />
        <p
          style={{ padding: 20, color: 'white', fontSize: 20, fontWeight: 100 }}
        >
          Raven <span style={{ fontSize: 16, fontWeight: 100, opacity: 0.6}}>{'v0.1a'}</span>
        </p>
      </div>
    );
  }
}
