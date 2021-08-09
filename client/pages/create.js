import Head from 'next/head'
import Link from 'next/link'
import {Formik} from "formik";
import {useRouter} from 'next/router'
import React, {useState} from "react";

const axios = require('axios');

export default function CreateAlerts() {
  const router = useRouter()
  const [non_field_error, setNonFieldError] = useState([])
  return (
    <div>
      <Head>
        <title>Create an alert</title>
      </Head>

      <main>
          <nav>
            <ul>
                <li>
                    <Link href={"/"}>
                        <a>Alert List</a>
                    </Link>
                </li>
                <li>
                    <Link href={"/create"}>
                        <a>Create Alert</a>
                    </Link>
                </li>
            </ul>
          </nav>
          <h1>Create an alert</h1>

          <Formik
                initialValues={{search_phrase: '', email: '', time_interval:""}}
                validate={values => {
                    return {};
                }}
                onSubmit={(values, {setSubmitting, setFieldError}) => {
                    const url = "http://127.0.0.1:8000/alerts/"
                    axios.post(
                        url, values,

                    )
                        .then(() => {
                            alert("Successfully Added.");
                            router.push("/")
                        })
                        .catch(err => {
                            const response = JSON.parse(err.response.request.response)
                            for (const [key, values] of Object.entries(response)) {
                                console.log(key)
                                console.log(values)
                                setFieldError(key, values[0])
                            }
                            if (response.hasOwnProperty("non_field_errors")){
                                setNonFieldError(response.non_field_errors)
                            }

                        }).finally(() => {
                        setSubmitting(false)
                    });
                }
                }
            >
                {({   errors,
                      values,
                      touched,
                      handleChange,
                      handleBlur,
                      handleSubmit,
                      isSubmitting,
                  }) => (



                        <form onSubmit={handleSubmit}>

                            {non_field_error.map( err => (
                                <div className={"error"}>
                                      {err}
                                </div>
                            ))}

                            <div>
                                <label htmlFor={"search_phrase_input"}>Search Phrase</label>
                                <input
                                    id={"search_phrase_input"}
                                    type="text"
                                    placeholder="Search  phrase e.g. playstation"
                                    name="search_phrase"
                                    onChange={handleChange}
                                    onBlur={handleBlur}
                                    value={values.name}
                                    required={true}

                                />
                                {errors.search_phrase &&
                                    touched.search_phrase &&
                                    <div className={"error"}>
                                      {errors.search_phrase}
                                    </div>}
                            </div>
                            <div>
                                <label htmlFor={"email_input"}>Search Phrase</label>
                                <input
                                    id={"email_input"}
                                    type="email"
                                    placeholder="John.Doe@example.com"
                                    name="email"
                                    onChange={handleChange}
                                    onBlur={handleBlur}
                                    value={values.name}
                                    required={true}

                                />
                                {errors.email &&
                                    touched.email &&
                                    <div className={"error"}>
                                      {errors.email}
                                    </div>}
                            </div>
                            <div>
                                <label htmlFor="time_interval_input" style={{ display: 'block' }}>
                                    Alert Interval
                                  </label>
                                  <select
                                    id={"time_interval_input"}
                                    name="time_interval"
                                    value={values.color}
                                    onChange={handleChange}
                                    onBlur={handleBlur}
                                    style={{ display: 'block' }}
                                    required={true}
                                  >
                                    <option value="" label="Select a time interval" />
                                    <option value="2" label="2 minutes" />
                                    <option value="5" label="5 minutes" />
                                    <option value="20" label="20 minutes" />
                                  </select>
                                  {errors.time_interval &&
                                    touched.time_interval &&
                                    <div className={"error"}>
                                      {errors.time_interval}
                                    </div>}
                            </div>

                            <button type="submit" disabled={isSubmitting}>Submit</button>
                        </form>
                    )}

            </Formik>
      </main>

    </div>
  )
}
