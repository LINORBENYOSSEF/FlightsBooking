
function flightHtml(flight) {
    return `
    <div class="card bg-secondary" data-flight-id="${flight.id}">
        <div name="flight-root" class="card-body" onclick="viewFlight('${flight.id}')">
            <h6 class="side-by-side-header">
                ${flight.departure.city}, ${flight.departure.country} ->
                ${flight.destination.city}, ${flight.destination.country}
            </h6>
            <div>${flight.airline.name}</div>
            <div>${flight.ticket_cost} $</div>
            <div>${new Date(flight.departure_time).toLocaleString()}</div>
        </div>
    </div>
    `;
}

function bookedFlightHtml(flight) {
    return `
    <div class="card bg-secondary">
        <div name="flight-root" class="card-body" data-flight-id="${flight.id}">
            <h6 class="side-by-side-header">
                ${flight.departure.city}, ${flight.departure.country} ->
                ${flight.destination.city}, ${flight.destination.country}
            </h6>
            <div>${flight.airline.name}</div>
            <div>${flight.paid} $</div>
            <div>${new Date(flight.departure_time).toLocaleString()}</div>
        </div>
    </div>
    `;
}

function loadFlights(offset,
                    limit,
                    reload = false,
                    callback = null) {
    $.ajax({
        method: "GET",
        url: "/api/flight/",
        contentType: "application/json",
        data: {
            limit: limit,
            offset: offset
        }
    }).done(function(data) {
        if (reload) {
            $('#flights-container').empty();
        }
        $.each(data, function(i, item) {
            $('#flights-container').append(flightHtml(item));
        });

        if (callback != null) {
            callback(data.length);
        }
    });
}

function openAddFlightModal() {
    var modal = $('#add-flight-modal');
    modal.modal('toggle');
}

function viewFlight(flightId) {
    $.ajax({
        method: "GET",
        url: `/api/flight/${flightId}`,
        contentType: "application/json"
    }).done(function(data) {
        console.log(data);
        var modal = $('#view-flight-modal');

        modal.find('.modal-title').html(flightId);
        modal.find('input[name="time-field"]').val(`${new Date(data.departure_time).toLocaleString()}`);
        modal.find('input[name="departure-field"]').val(`${data.departure.city}, ${data.departure.country}`);
        modal.find('input[name="destination-field"]').val(`${data.destination.city}, ${data.destination.country}`);
        modal.find('input[name="price-field"]').val(`${data.ticket_cost} Dollars`);
        modal.modal('toggle');
    });
}

function addFlight() {
    var modal = $('#add-flight-modal');

    var airlineName = $('#airline-name').val();
    var departureCity = $('#departure-city').val();
    var departureCountry = $('#departure-country').val();
    var destinationCity = $('#destination-city').val();
    var destinationCountry = $('#destination-country').val();
    var datetime = $('#datetime').val();
    var ticketCost = $('#ticket-cost').val();

    $.ajax({
        method: "POST",
        url: `/api/flight/`,
        contentType: "application/json",
        data: JSON.stringify({
            airline: {
                name: airlineName
            },
            departure_time: datetime,
            departure: {
                city: departureCity,
                country: departureCountry
            },
            destination: {
                city: destinationCity,
                country: destinationCountry
            },
            ticket_cost: ticketCost
        })
    }).done(function(data) {
        modal.modal('toggle');

        var container = $('#flights-container');
        container.append(flightHtml(data));
    });
}

function bookFlight() {
    var modal = $('#view-flight-modal');
    var flightId = modal.find('.modal-title').html();
    $.ajax({
        method: "POST",
        url: `/api/flight/${flightId}/book/`,
        contentType: "application/json"
    }).done(function(data) {
        console.log(data);
        alert('Booked!');
    }).fail(function(xhr, ajaxOptions, thrownError) {
        alert('Error Booking');
    });
}

function deleteFlight() {
    var modal = $('#view-flight-modal');
    var flightId = modal.find('.modal-title').html();
    $.ajax({
        method: "DELETE",
        url: `/api/flight/${flightId}/`,
        contentType: "application/json"
    }).done(function(data) {
        modal.modal('toggle');

        var container = $('#flights-container');
        var flight = container.find(`div[data-flight-id="${flightId}"]`);
        flight.remove();
    });
}

function loadBookedFlights() {
    $.ajax({
        method: "GET",
        url: "/api/flight/booked/",
        contentType: "application/json"
    }).done(function(data) {
        $.each(data, function(i, item) {
            $('#flights-container').append(bookedFlightHtml(item));
        });
    });
}
