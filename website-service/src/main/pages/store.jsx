import React, { PropTypes } from 'react'


export default class Store extends React.Component {
  static propTypes = {
    children: PropTypes.any.isRequired,
  }

  render() {
    return (
      <div>
        <h1 className="ui center aligned header">Store</h1>
        {this.props.children}
      </div>
    )
  }
}
