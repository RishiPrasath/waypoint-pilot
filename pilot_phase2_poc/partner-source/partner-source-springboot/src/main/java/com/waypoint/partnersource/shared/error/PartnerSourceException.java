package com.waypoint.partnersource.shared.error;

import org.springframework.http.HttpStatus;

public class PartnerSourceException extends RuntimeException {
    private final HttpStatus status;
    private final ErrorCode errorCode;
    private final String title;

    public PartnerSourceException(HttpStatus status, ErrorCode errorCode, String title, String detail) {
        super(detail);
        this.status = status;
        this.errorCode = errorCode;
        this.title = title;
    }

    public static PartnerSourceException invalidRequest(String detail) {
        return new PartnerSourceException(HttpStatus.BAD_REQUEST, ErrorCode.INVALID_REQUEST,
                "Invalid request", detail);
    }

    public static PartnerSourceException orderNotFound(String orderId) {
        return new PartnerSourceException(HttpStatus.NOT_FOUND, ErrorCode.ORDER_NOT_FOUND,
                "Order not found", "No order exists for orderId " + orderId + ".");
    }

    public static PartnerSourceException driverNotFound(String driverId) {
        return new PartnerSourceException(HttpStatus.NOT_FOUND, ErrorCode.DRIVER_NOT_FOUND,
                "Driver not found", "No driver exists for driverId " + driverId + ".");
    }

    public static PartnerSourceException orderNotAssignedToDriver(String orderId, String driverId) {
        return new PartnerSourceException(HttpStatus.FORBIDDEN, ErrorCode.ORDER_NOT_ASSIGNED_TO_DRIVER,
                "Order not assigned to driver", "Driver " + driverId + " is not assigned to order " + orderId + ".");
    }

    public static PartnerSourceException invalidStatusTransition(String detail) {
        return new PartnerSourceException(HttpStatus.CONFLICT, ErrorCode.INVALID_STATUS_TRANSITION,
                "Invalid status transition", detail);
    }

    public static PartnerSourceException invalidStatusEvent(String detail) {
        return new PartnerSourceException(HttpStatus.UNPROCESSABLE_CONTENT, ErrorCode.INVALID_STATUS_EVENT,
                "Invalid status event", detail);
    }

    public HttpStatus status() {
        return status;
    }

    public ErrorCode errorCode() {
        return errorCode;
    }

    public String title() {
        return title;
    }
}
