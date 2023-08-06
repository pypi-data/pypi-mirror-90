import maglev
import reservedseating

from typing import Any, List, Callable

class ReservedSeating:
	"""
	An Library for Reserved Seating
	Venues have Seats, Events are at Venues
	Reservations are Seats at Events
	"""
	def __init__(self):
		bus = maglev.maglev_MagLev.getInstance("default")
		lib = reservedseating.reservedseating_ReservedSeating(bus)

	def CreateVenue(self, ownerId: str, name: str, maxPeople: float) -> str:
		"""		Create a new venue
		Args:
			ownerId (str):Who is responsible for this venue
			name (str):Name of Venue
			maxPeople (float):Maximum people permitted in venue
		Returns:
			the id of the new venue
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [ownerId, name, maxPeople]
		ret = None
		def CreateVenue_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ReservedSeating.CreateVenue', args, CreateVenue_Ret)
		return ret

	def CreateVenueConfiguration(self, venueId: str, name: str, maxPeople: float) -> str:
		"""		Create a new Venue Congiguration
		Args:
			venueId (str):Venue
			name (str):Name of Venue Configuration
			maxPeople (float):Maximum number of people permitted in this Venue Configuration
		Returns:
			the id of the new Venue Configuration
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [venueId, name, maxPeople]
		ret = None
		def CreateVenueConfiguration_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ReservedSeating.CreateVenueConfiguration', args, CreateVenueConfiguration_Ret)
		return ret

	def CreateSeat(self, name: str, seatClass: str, venueConfigId: str, nextTo: List[Any], tableId: str, geometry: object) -> str:
		"""		Create a new seat
		Args:
			name (str):The seat name
			seatClass (str):The class of seat
			venueConfigId (str):the Venue Configuration the seat belongs to
			nextTo (List[Any]):the seats that are next to this one
			tableId (str):the table this seat is at
			geometry (object):Information about where the Seat is
		Returns:
			the id of the new seat
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [name, seatClass, venueConfigId, nextTo, tableId, geometry]
		ret = None
		def CreateSeat_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ReservedSeating.CreateSeat', args, CreateSeat_Ret)
		return ret

	def CreateEvent(self, ownerId: str, venueConfigId: str, maxPeople: float) -> str:
		"""		Create a new Event
		Args:
			ownerId (str):Who is responsible for this event
			venueConfigId (str):Venue Configuration to use for this event
			maxPeople (float):Maximum people permitted in venue
		Returns:
			the id of the new Event
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [ownerId, venueConfigId, maxPeople]
		ret = None
		def CreateEvent_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ReservedSeating.CreateEvent', args, CreateEvent_Ret)
		return ret

	def CreateTable(self, venueConfigId: str, minSeats: float, maxSeats: float, geometry: object) -> str:
		"""		Create a new Table
		Args:
			venueConfigId (str):Venue Configuration to use for this event
			minSeats (float):Minimum number of people in a party to reserve the table
			maxSeats (float):Maximum number of people that can sit at this table
			geometry (object):Information about where the Table is
		Returns:
			the id of the new Table
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [venueConfigId, minSeats, maxSeats, geometry]
		ret = None
		def CreateTable_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ReservedSeating.CreateTable', args, CreateTable_Ret)
		return ret

	def CreateOrder(self, userId: str, eventId: str, expires: float) -> str:
		"""		Create a new Order
		Args:
			userId (str):The user who is placing the reservation
			eventId (str):The event that the order is for
			expires (float):Timestamp when order expires and is considered abondoned
		Returns:
			the id of the new Order
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [userId, eventId, expires]
		ret = None
		def CreateOrder_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ReservedSeating.CreateOrder', args, CreateOrder_Ret)
		return ret

	def GetVenue(self, id: str) -> object:
		"""		Get a Venue
		Args:
			id (str):Venue ID
		Returns:
			the Venue data as an object
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [id]
		ret = None
		def GetVenue_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ReservedSeating.GetVenue', args, GetVenue_Ret)
		return ret

	def GetVenueConfiguration(self, id: str) -> object:
		"""		Get a Venue Configuration
		Args:
			id (str):Venue Configuration ID
		Returns:
			the VenueConfiguration data as an object
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [id]
		ret = None
		def GetVenueConfiguration_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ReservedSeating.GetVenueConfiguration', args, GetVenueConfiguration_Ret)
		return ret

	def GetSeat(self, id: str) -> object:
		"""		Get a Seat
		Args:
			id (str):Seat ID
		Returns:
			the Seat data as an object
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [id]
		ret = None
		def GetSeat_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ReservedSeating.GetSeat', args, GetSeat_Ret)
		return ret

	def GetEvent(self, id: str) -> object:
		"""		Get an Event
		Args:
			id (str):Event ID
		Returns:
			the Event data as an object
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [id]
		ret = None
		def GetEvent_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ReservedSeating.GetEvent', args, GetEvent_Ret)
		return ret

	def GetTable(self, id: str) -> object:
		"""		Get a Table
		Args:
			id (str):Table ID
		Returns:
			the Table data as an object
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [id]
		ret = None
		def GetTable_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ReservedSeating.GetTable', args, GetTable_Ret)
		return ret

	def UpdateVenue(self, data: object, complete: bool):
		"""		Update a Venue
		Args:
			data (object):Venue data to update
			complete (bool):if set to true, missing fields should be deleted
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [data, complete]
		ret = None
		def UpdateVenue_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ReservedSeating.UpdateVenue', args, UpdateVenue_Ret)

	def UpdateVenueConfiguration(self, data: object, complete: bool):
		"""		Update a Venue Configuration
		Args:
			data (object):Venue Configuration data to update
			complete (bool):if set to true, missing fields should be deleted
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [data, complete]
		ret = None
		def UpdateVenueConfiguration_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ReservedSeating.UpdateVenueConfiguration', args, UpdateVenueConfiguration_Ret)

	def UpdateSeat(self, data: object, complete: bool):
		"""		Update a Seat
		Args:
			data (object):Seat data to update
			complete (bool):if set to true, missing fields should be deleted
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [data, complete]
		ret = None
		def UpdateSeat_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ReservedSeating.UpdateSeat', args, UpdateSeat_Ret)

	def UpdateEvent(self, data: object, complete: bool):
		"""		Update an Event
		Args:
			data (object):Event data to update
			complete (bool):if set to true, missing fields should be deleted
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [data, complete]
		ret = None
		def UpdateEvent_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ReservedSeating.UpdateEvent', args, UpdateEvent_Ret)

	def UpdateTable(self, data: object, complete: bool):
		"""		Update a Table
		Args:
			data (object):Table data to update
			complete (bool):if set to true, missing fields should be deleted
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [data, complete]
		ret = None
		def UpdateTable_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ReservedSeating.UpdateTable', args, UpdateTable_Ret)

	def DeleteVenue(self, id: str):
		"""		Delete a Venue
		Args:
			id (str):Venue ID
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [id]
		ret = None
		def DeleteVenue_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ReservedSeating.DeleteVenue', args, DeleteVenue_Ret)

	def DeleteVenueConfiguration(self, id: str):
		"""		Delete a Venue Configuration
		Must be unavailable first
		Args:
			id (str):Venue Configuration ID
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [id]
		ret = None
		def DeleteVenueConfiguration_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ReservedSeating.DeleteVenueConfiguration', args, DeleteVenueConfiguration_Ret)

	def DeleteSeat(self, id: str):
		"""		Delete a Seat
		Venue Configuration must be unavailable first
		Args:
			id (str):Seat ID
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [id]
		ret = None
		def DeleteSeat_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ReservedSeating.DeleteSeat', args, DeleteSeat_Ret)

	def DeleteEvent(self, id: str):
		"""		Delete an Event
		Events on sale must be cancelled before being deleted.
		Args:
			id (str):Event ID
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [id]
		ret = None
		def DeleteEvent_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ReservedSeating.DeleteEvent', args, DeleteEvent_Ret)

	def DeleteTable(self, id: str):
		"""		Delete a Table
		Venue Configuration must be unavailable first
		Args:
			id (str):Table ID
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [id]
		ret = None
		def DeleteTable_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ReservedSeating.DeleteTable', args, DeleteTable_Ret)

	def DeleteOrder(self, id: str):
		"""		Delete an Order
		Reservations must be cancelled first
		Args:
			id (str):Order ID
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [id]
		ret = None
		def DeleteOrder_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ReservedSeating.DeleteOrder', args, DeleteOrder_Ret)

	def CompleteOrder(self, orderId: str):
		"""		Complete order and convert holds into reservations
		Args:
			orderId (str):Order ID
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [orderId]
		ret = None
		def CompleteOrder_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ReservedSeating.CompleteOrder', args, CompleteOrder_Ret)

	def AddSeatToOrder(self, orderId: str, seatId: str):
		"""		Place a hold on a seat and add it to an order
		Args:
			orderId (str):Order ID
			seatId (str):Seat ID
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [orderId, seatId]
		ret = None
		def AddSeatToOrder_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ReservedSeating.AddSeatToOrder', args, AddSeatToOrder_Ret)

	def ContinueOrder(self, orderId: str, expires: float):
		"""		Keep an order from expiring and becoming abondoned
		Args:
			orderId (str):Order ID
			expires (float):New timestamp when order will expire
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [orderId, expires]
		ret = None
		def ContinueOrder_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ReservedSeating.ContinueOrder', args, ContinueOrder_Ret)

	def AutoSelect(self, numSeats: float, seatClassPreference: List[Any]):
		"""		Automatically select some seats and add them to the order
		Args:
			numSeats (float):Number of seats to select
			seatClassPreference (List[Any]):Which seat classes to prefer in order
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [numSeats, seatClassPreference]
		ret = None
		def AutoSelect_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ReservedSeating.AutoSelect', args, AutoSelect_Ret)

	def CancelEvent(self, eventId: str):
		"""		Cancel an event and all reservations for that event
		Args:
			eventId (str):Event ID
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [eventId]
		ret = None
		def CancelEvent_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ReservedSeating.CancelEvent', args, CancelEvent_Ret)

	def CancelReservation(self, orderId: str, seatId: str):
		"""		Cancel a reservation and release the seats
		Args:
			orderId (str):Order ID
			seatId (str):Seat ID
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [orderId, seatId]
		ret = None
		def CancelReservation_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ReservedSeating.CancelReservation', args, CancelReservation_Ret)

	def GetSeatsAndTablesForEvent(self, eventId: str, page: float, perpage: float):
		"""		Get all Seats and Tables for an Event
		Args:
			eventId (str):Event ID
			page (float):page number
			perpage (float):per page
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [eventId, page, perpage]
		ret = None
		def GetSeatsAndTablesForEvent_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ReservedSeating.GetSeatsAndTablesForEvent', args, GetSeatsAndTablesForEvent_Ret)

	def FindAbandonedOrders(self, page: float, perpage: float) -> List[Any]:
		"""		Get any abondoned (expired) orders
		Args:
			page (float):page number
			perpage (float):per page
		Returns:
			abondoned orders
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [page, perpage]
		ret = None
		def FindAbandonedOrders_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ReservedSeating.FindAbandonedOrders', args, FindAbandonedOrders_Ret)
		return ret

	def GetOrdersForUser(self, userId: str, page: float, perpage: float) -> List[Any]:
		"""		Get a users orders
		Args:
			userId (str):User ID
			page (float):page number
			perpage (float):per page
		Returns:
			orders for user
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [userId, page, perpage]
		ret = None
		def GetOrdersForUser_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ReservedSeating.GetOrdersForUser', args, GetOrdersForUser_Ret)
		return ret

	def GetAllEventsOnSale(self, page: float, perpage: float) -> List[Any]:
		"""		Get all Events marked on sale
		Args:
			page (float):page number
			perpage (float):per page
		Returns:
			events on sale
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [page, perpage]
		ret = None
		def GetAllEventsOnSale_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ReservedSeating.GetAllEventsOnSale', args, GetAllEventsOnSale_Ret)
		return ret

	def UpdateVenueConfigurationAvailability(self, venueConfigurationId: str, available: bool):
		"""		Make a venue configuration available or unavailable.
		Must not have any events for sale using this venute configuration.
		Args:
			venueConfigurationId (str):Venue Configuration ID
			available (bool):availability
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [venueConfigurationId, available]
		ret = None
		def UpdateVenueConfigurationAvailability_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ReservedSeating.UpdateVenueConfigurationAvailability', args, UpdateVenueConfigurationAvailability_Ret)

	def GetVenueConfigurations(self, venueId: str) -> List[Any]:
		"""		Get Venue Configurations for a Venue
		Args:
			venueId (str):Venue ID
		Returns:
			the Venue Configurations for the specified Venue
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [venueId]
		ret = None
		def GetVenueConfigurations_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ReservedSeating.GetVenueConfigurations', args, GetVenueConfigurations_Ret)
		return ret

	def GetOrderSummary(self, orderId: str) -> List[Any]:
		"""		Get a summary of an Order
		Args:
			orderId (str):Order ID
		Returns:
			the summary for the specified Order
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [orderId]
		ret = None
		def GetOrderSummary_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ReservedSeating.GetOrderSummary', args, GetOrderSummary_Ret)
		return ret

	def GetAllVenuesByOwner(self, ownerId: str) -> List[Any]:
		"""		Get all Venues for an owner
		Args:
			ownerId (str):owner id
		Returns:
			List of venues
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [ownerId]
		ret = None
		def GetAllVenuesByOwner_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ReservedSeating.GetAllVenuesByOwner', args, GetAllVenuesByOwner_Ret)
		return ret



