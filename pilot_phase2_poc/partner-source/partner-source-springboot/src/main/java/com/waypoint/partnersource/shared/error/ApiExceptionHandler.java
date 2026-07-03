package com.waypoint.partnersource.shared.error;

import jakarta.servlet.http.HttpServletRequest;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.method.annotation.HandlerMethodValidationException;
import org.springframework.web.method.annotation.MethodArgumentTypeMismatchException;

@RestControllerAdvice
public class ApiExceptionHandler {
    private final ProblemDetailFactory problemDetailFactory = new ProblemDetailFactory();

    @ExceptionHandler(PartnerSourceException.class)
    public ResponseEntity<ProblemDetailResponse> handlePartnerSourceException(
            PartnerSourceException exception,
            HttpServletRequest request
    ) {
        var problem = problemDetailFactory.from(request, exception);
        return ResponseEntity.status(exception.status())
                .contentType(MediaType.APPLICATION_PROBLEM_JSON)
                .body(problem);
    }

    @ExceptionHandler({
            MethodArgumentNotValidException.class,
            HandlerMethodValidationException.class,
            MethodArgumentTypeMismatchException.class,
            HttpMessageNotReadableException.class
    })
    public ResponseEntity<ProblemDetailResponse> handleValidationException(Exception exception, HttpServletRequest request) {
        var error = PartnerSourceException.invalidRequest("Request validation failed.");
        var problem = problemDetailFactory.from(request, error);
        return ResponseEntity.badRequest()
                .contentType(MediaType.APPLICATION_PROBLEM_JSON)
                .body(problem);
    }
}
