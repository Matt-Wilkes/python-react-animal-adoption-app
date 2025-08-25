import { Alert, Box, Container, Stack, TextField, Typography } from '@mui/material'
import {React, useState} from 'react'
import Button from '@mui/material/Button'
import { useAuth } from "../../components/Context/AuthProvider"

export const ForgottenPasswordPage = () => {
    const {sendForgottenPassword} = useAuth()
    const [email, setEmail] = useState("")
    const [submitted, setSubmitted] = useState(false)

    const handleEmailChange = (event) => {
    setEmail(event.target.value);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        setSubmitted(false)
        console.log('clicked')
        console.log('email:', email)
        try {
            const response = await sendForgottenPassword(email);
            console.log(response)
            setSubmitted(true)
        } catch (error) {
            console.log(error)
        }
    }




  return (
    <Container
    sx={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '90vh',
    }}
    >
        <Stack
        sx={{
            backgroundColor: 'white',
            height: 'max-content',
            padding: 2,
            borderRadius: 1,
            width: 300
        }}
        component="form"
        id='forgotten-password-form'
        onSubmit={handleSubmit}
        >
        <Typography
        variant='body1'
        color={'black'}
        >Please fill in your email address below</Typography>
        <TextField 
        sx={{
            marginTop: 2
        }}
        label='Email address'
        variant='outlined'
        required
        id='email-input'
        onChange={handleEmailChange}
        >

        </TextField>
        <Button
        sx={{
            marginTop: 2
        }}
        type='submit'
        id='submit-button'
        form='forgotten-password-form'
        variant='contained'
        disableElevation
        >Submit</Button>
        {submitted && (
            <Alert
        severity='success'
        sx={{
            marginTop: 2
        }}
        >If the account exists, A password reset email has been sent

        </Alert>
        )}
    </Stack>
    </Container>
    
  )
}

export default ForgottenPasswordPage