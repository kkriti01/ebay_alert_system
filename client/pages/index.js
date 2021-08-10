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
                <li>
                    <Link href={"/"}>
                        <a><u>Alert List</u></a>
                    </Link>
                </li>
                <li>
                    <Link href={"/create"}>
                        <a>Create Alert</a>
                    </Link>
                </li>
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
                   <tr key={alert.id}>
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

export async function getServerSideProps(context) {
    const url = `${process.env.SERVER_API_HOST}/alerts/`
    const res = await fetch(url);
    const alerts = await res.json();

    return {
        props: {
            alerts: alerts
        },
    }
}
