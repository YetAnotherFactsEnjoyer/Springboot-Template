package com.example.starter.shared.exception;

import java.time.Instant;

public record ApiError(
    String code,
    String message,
    Instant timestamp
) {
}
