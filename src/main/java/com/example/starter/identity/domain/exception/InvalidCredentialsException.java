package com.example.starter.identity.domain.exception;

public class InvalidCredentialsException extends RuntimeException {

    public InvalidCredentialsException() {
        super("Invalid email or password");
    }
}
