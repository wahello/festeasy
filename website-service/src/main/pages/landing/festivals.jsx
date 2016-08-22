import React, { PropTypes } from 'react'
import { Link } from 'react-router'
import {
  Header,
  Content,
  Grid,
  Row,
  Column,
  Description,
  Cards,
  Card,
} from 'semantic-react'
import SelectFestivalButton from 'main/components/selectFestivalButton.jsx'


export default class FestivalsContainer extends React.Component {
  static contextTypes = {
    store: PropTypes.object.isRequired,
  }

  constructor() {
    super()
    this.state = {
      festivals: null,
    }
    this.fetchFestivals = this.fetchFestivals.bind(this)
  }

  componentDidMount() {
    this.fetchFestivals()
  }

  fetchFestivals() {
    this.context.store.findAll(
      'festival',
    )
    .then((festivals) => {
      this.setState({ festivals })
    })
  }

  render() {
    let festivals = []
    if (this.state.festivals) {
      festivals = this.state.festivals.map((f) => (
        <Card
          key={f.id}
          style={{ height: 200 }}
        >
          <Content>
            <Header>
              <Link
                to={`/festivals/${f.id}`}
              >
                {f.name}
              </Link>
            </Header>
            <Description>
              {f.description}
            </Description>
            <SelectFestivalButton style={{ zIndex: 999 }} festival={f} />
          </Content>
        </Card>
      ))
    }
    return (
      <div style={{ paddingTop: 30 }}>
        <Header
          aligned="center"
          size="huge"
          style={{
            fontSize: 60,
          }}
        >
          find your festival
        </Header>
        <Grid style={{ fontSize: 20 }}>
          <Row>
            <Column aligned="center">
              <p>
                We offer our services to every major festival in the Western Cape.
              </p>
            </Column>
          </Row>
          <Row>
            <Column aligned="center">
              <p>
                As our customer base grows, so will our festival selection
                , as we aim to move to every festival in South Africa and... the World.
              </p>
            </Column>
          </Row>
        </Grid>
        <div className="ui container">
          <Cards className="three">
            {festivals}
          </Cards>
          <Grid aligned="center">
            <Column>
              <Link
                to="/festivals"
                className="ui massive yellow button"
              >
                See All Festivals
              </Link>
            </Column>
          </Grid>
        </div>
      </div>
    )
  }
}
