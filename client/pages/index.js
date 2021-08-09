import Head from 'next/head'
import Link from 'next/link'

export default function Alerts(props) {
  return (
    <div>
      <Head>
        <title>Alert</title>
      </Head>
      <main>
          <nav>
            <ul>
                <li><Link href={"/"}><a>Alert List</a></Link></li>
                <li><Link href={"/create"}><a>Create Alert</a></Link></li>
            </ul>
          </nav>
          <h1>Alert Lists</h1>
          <table>
              <thead>
                <tr>
                    <th>Search Phrase</th>
                    <th>Interval</th>
                    <th>Email</th>
                    <th>Created on</th>
                </tr>
              </thead>
              <tbody>
               {props.alerts.map(alert => (
                   <tr>
                       <td>{alert.search_phrase}</td>
                       <td>{alert.time_interval} minutes</td>
                       <td>{alert.email}</td>
                       <td>{alert.created_at}</td>
                   </tr>
               ))}
              </tbody>
          </table>
      </main>

    </div>
  )
}

export async function getStaticProps(context) {
    const url = "http://127.0.0.1:8000/alerts/"

    const res = await fetch(url, {
    });
    const alerts = await res.json();

    return {
        props: {
            alerts: alerts
        },
    }
}
